import datetime
import flask_login
from collections import namedtuple
from flask import current_app as app
from flask_login import login_required
from concurrent.futures import ThreadPoolExecutor
from erp.marketing.campaign.Mail import SendMail
from erp.contacts.contact import Contact as customer_contact
from erp.general import is_already_added, tobe_deleted_items
from erp.marketing.campaign.sms import SendSMS, cached, TTLCache
from flask import Blueprint, url_for, redirect, render_template, request
from erp.models.harlos_db import (
    db,
    Users,
    Campaign,
    UserRoles,
    ContactGroups,
    ItemsToDelete,
)


marketing_bp = Blueprint(
    "marketing_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

contact_book = customer_contact()
mail = SendMail()
sms_sender = SendSMS()


def load_all_groups():
    groups = ContactGroups.query.order_by(ContactGroups.date_created.desc()).all()
    return groups if groups else []


@cached(cache=TTLCache(maxsize=1024, ttl=5))
def load_summary_data():
    brief_summary = namedtuple(
        "Highlight_Summary", "total_contacts remaining_sms no_of_campaigns"
    )
    with app.app_context():
        no_of_campaigns = (
            0 if not Campaign.query.count() else Campaign.query.count()
        )  # set time out for opec get sms api

        try:
            return brief_summary(
                contact_book.contact_count, sms_sender.get_balance, no_of_campaigns
            )
        except Exception as bug:
            print(bug)
            return brief_summary(contact_book.contact_count, 0, no_of_campaigns)


@cached(cache=TTLCache(maxsize=1024, ttl=5))
def load_all_campaigns():
    try:
        with app.app_context():
            campaigns = Campaign.query.all()
            if campaigns:
                return campaigns
        return []
    except Exception as bug:
        print(bug)
        return False


def thread_number(no_contacts_book):
    print(no_contacts_book)
    if len(no_contacts_book) < 10:
        return len(no_contacts_book)
    return 10


def send_sms_campaign(
    campaign_name: str, campaign_message: str, contact_type: str = "All"
):
    try:
        with app.app_context():
            sms_contacts = contact_book.load_customer_phones(status=contact_type)
            print(sms_contacts, "sms contacts")
            if sms_contacts:
                with ThreadPoolExecutor(
                    max_workers=thread_number(sms_contacts)
                ) as compiler:
                    for campaign_contact in sms_contacts:
                        compiler.submit(
                            sms_sender.send_sms,
                            message=campaign_message,
                            mobile_no=campaign_contact.phone,
                        )

                new_campaign = Campaign(
                    user_id=flask_login.current_user.user_id,
                    campaign_name=campaign_name,
                    contact_type=contact_type,
                    campaign_type="SMS-Marketing",
                    campaign_status="Complete",
                    campaign_message=campaign_message,
                    audience_reached=len(sms_contacts),
                )

                db.session.add(new_campaign)
                db.session.commit()
                print("campaign accomplished")
                return True
            print("no contact found  therefore Campaign Failed")
    except Exception as bug:
        print(bug)
        print("mmmmh")
        return


def send_email_campaign(campaign_name: str, message: str, contact_type: str):
    try:
        recipients = contact_book.load_customer_emails(status=contact_type)
        if recipients and message:
            mail.send_mail(message=message, recipients=recipients)

            new_campaign = Campaign(
                user_id=flask_login.current_user.user_id,
                campaign_name=campaign_name,
                contact_type=contact_type,
                campaign_type="Email-Marketing",
                campaign_message=message,
                campaign_status="Complete",
                audience_reached=len(recipients),
            )

            db.session.add(new_campaign)
            db.session.commit()
            return True

        print("No recipients or message found")
        return False
    except Exception as bug:
        print(bug)
        return


def format_the_date(raw_date: str):
    try:
        year, month, day = [int(duration) for duration in raw_date.split("/")]
        return datetime.date(year, month, day)
    except Exception as bug:
        try:
            year, month, day = [int(duration) for duration in raw_date.split("-")]
            return datetime.date(year, month, day)
        except Exception as bug:
            print(bug)
            print(f"{raw_date} should be formatted correctly")
            return None


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get current role")
        print(bug)
        return None


def add_custom_marketing(campaign_data: dict) -> bool:
    with app.app_context():
        campaign_owner = campaign_data.get("campaign_owner")
        campaign_name = campaign_data.get("campaign_name")
        campaign_type = campaign_data.get("campaign_type")
        campaign_status = campaign_data.get("campaign_status")
        description = campaign_data.get("description")
        audience_reached = campaign_data.get("audience_reached")
        expected_revenue = campaign_data.get("expected_revenue")
        actual_cost = campaign_data.get("actual_cost")
        budgeted_cost = campaign_data.get("budgeted_cost")
        expected_response = campaign_data.get("expected_response")
        start_date = campaign_data.get("start_date")
        end_date = campaign_data.get("end_date")
        actual_cost = actual_cost if actual_cost else 0.0
        budgeted_cost = budgeted_cost if budgeted_cost else 0.0
        expected_revenue = expected_revenue if expected_revenue else 0.0
        start_date = format_the_date(start_date) if start_date else None
        end_date = format_the_date(end_date) if end_date else None
        user_id = flask_login.current_user.user_id
        try:
            new_campaign = Campaign(
                user_id=user_id,
                campaign_owner=campaign_owner,
                campaign_name=campaign_name,
                campaign_type=campaign_type,
                campaign_status=campaign_status,
                description=description,
                audience_reached=audience_reached,
                actual_cost=actual_cost,
                budgeted_cost=budgeted_cost,
                expected_revenue=expected_revenue,
                expected_response=expected_response,
                start_date=start_date,
                end_date=end_date,
            )

            db.session.add(new_campaign)
            db.session.commit()
            print("Custom marketing added")
            return True
        except Exception as bug:
            print(bug)
            return False


@marketing_bp.route("/marketing")
@login_required
def marketing():
    current_user = get_current_role()
    if current_user.can_view_marketing:
        return render_template(
            "marketing.html",
            title="Marketing",
            highlights=load_summary_data(),
            role=get_current_role(),
        )
    return redirect(url_for("home_bp._401"))


@marketing_bp.route("/marketing/sms-campaign", methods=["GET", "POST"])
@login_required
def sms_marketing():
    current_user = get_current_role()
    if current_user.can_do_marketing:
        if request.method == "POST":
            campaign_name = request.form.get("campaign_name")
            campaign_message = request.form.get("campaign_message")
            contact_type = request.form.get("contact_type")
            print(campaign_name, campaign_message, contact_type)
            send_sms_campaign(
                campaign_name=campaign_name,
                campaign_message=campaign_message,
                contact_type=contact_type,
            )
            return redirect(url_for("marketing_bp.marketing"))
        return render_template(
            "sms-campaign.html",
            title="Marketing| SMS Campaign",
            groups=load_all_groups(),
        )
    return redirect(url_for("home_bp._401"))


@marketing_bp.route("/marketing/email-campaign", methods=["GET", "POST"])
@login_required
def email_marketing():
    current_user = get_current_role()
    if current_user.can_do_marketing:
        if request.method == "POST":
            campaign_name = request.form.get("campaign_name")
            campaign_message = request.form.get("campaign_message")
            contact_type = request.form.get("contact_type")
            print(campaign_name, campaign_message, contact_type)
            send_email_campaign(
                campaign_name=campaign_name,
                message=campaign_message,
                contact_type=contact_type,
            )
            return redirect(url_for("marketing_bp.marketing"))
        return render_template(
            "email-campaign.html",
            title="Marketing | Email Campaign",
            groups=load_all_groups(),
        )
    return redirect(url_for("home_bp._401"))


@marketing_bp.route("/marketing/custom-campaign", methods=["GET", "POST"])
@login_required
def custom_marketing():
    current_user = get_current_role()
    if current_user.can_do_marketing:
        if request.method == "POST":
            add_custom_marketing(request.form)
            return redirect(url_for("marketing_bp.marketing"))
        else:
            return render_template(
                "custom-campaign.html", title="Marketing | Custom Campaign"
            )
    return redirect(url_for("home_bp._401"))


@marketing_bp.route("/marketing/campaigns-sent", methods=["GET", "POST"])
@login_required
def campaign_sent():
    current_user = get_current_role()
    if current_user.can_view_marketing:
        if request.method == "POST":
            campaign_id = request.form.get("campaign_id")
            status = request.form.get("status")
            campaign_id = int(campaign_id) if campaign_id.isdigit() else campaign_id
            campaign = Campaign.query.filter_by(campaign_id=campaign_id).first()
            campaign.campaign_status = status
            db.session.commit()
            print(status)
        return render_template(
            "campaign-sent.html",
            title="Marketing | Campaign Sent",
            all_campaigns=load_all_campaigns(),
            role=get_current_role(),
            d_campaigns=tobe_deleted_items("Campaign"),
        )
    return redirect(url_for("home_bp._401"))


@marketing_bp.route("/delete-campaign", methods=["POST"])
def delete_campaign():
    current_email = flask_login.current_user.email
    campaign_id = request.form.get("campaign_id")
    reason = request.form.get("reason")
    if is_already_added("Campaign", campaign_id):
        return redirect(url_for("marketing_bp.campaign_sent"))

    try:
        contact_to_delete = ItemsToDelete(
            item_id=campaign_id,
            table_name="Campaign",
            reason=reason,
            requested_by=current_email,
        )
        db.session.add(contact_to_delete)
        db.session.commit()
    except Exception as bug:
        print(bug)

    finally:
        return redirect(url_for("marketing_bp.campaign_sent"))
