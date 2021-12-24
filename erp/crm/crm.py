from erp.general import is_already_added, tobe_deleted_items
import json
import pycountry
import datetime
from types import ClassMethodDescriptorType
from typing import List, Union
import flask_login
from collections import namedtuple
from flask import current_app as app
from flask_login import login_required
from erp.settings.settings import load_all_settings
from erp.models.harlos_db import (
    ItemsToDelete,
    Users,
    db,
    Leads,
    Deals,
    Accounts,
    Activities,
    CrmContacts,
    CRM_Setting,
    UserRoles,
    InvoiceCounter,
    Campaign,
)
from flask import Blueprint, url_for, redirect, render_template, request


crm_bp = Blueprint(
    "crm_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def format_the_date(date: str):
    try:
        day, month, year = [int(duration) for duration in date.split("/")]
        return datetime.date(year, month, day)
    except Exception as bug:
        try:
            day, month, year = [int(duration) for duration in date.split("-")]
            return datetime.date(year, month, day)
        except Exception as bug:
            print(bug)
            print(f"{date} should be formatted correctly")
            return None


def current_user_role() -> Union[None, Users]:
    try:
        user_id = flask_login.current_user.user_id
        user_role_name = Users.query.filter_by(user_id=user_id).first().role
        return UserRoles.query.filter_by(role_name=user_role_name).first()
    except Exception as bug:
        print(bug)
        print("Bug occured while loading current user role")
        return


def get_all_countries():
    return list(pycountry.countries)


def add_leads_todb(form_data: dict, update: bool = False) -> bool:
    try:
        with app.app_context():
            city = form_data.get("city")
            email = form_data.get("email")
            phone = form_data.get("phone")
            country = form_data.get("country")
            industry = form_data.get("industry")
            company = form_data.get("company")
            persona = form_data.get("persona")
            firstname = form_data.get("firstname")
            lastname = form_data.get("lastname")
            address = form_data.get("address")
            group = form_data.get("group")
            lead_status = form_data.get("lead_status")
            lead_source = form_data.get("lead_source")
            description = form_data.get("description")
            lead_owner = flask_login.current_user.fullname
            lead_title = form_data.get("lead_title")
            lead_product = form_data.get("lead_product")

            if not update:
                new_lead = Leads(
                    firstname=firstname,
                    lastname=lastname,
                    city=city,
                    phone=phone,
                    country=country,
                    industry=industry,
                    company=company,
                    persona=persona,
                    email=email,
                    address=address,
                    group=group,
                    description=description,
                    lead_status=lead_status,
                    lead_source=lead_source,
                    lead_title=lead_title,
                    lead_product=lead_product,
                    lead_owner=lead_owner,
                )

                db.session.add(new_lead)
                db.session.commit()
                print("New Lead added")
                return True
            else:
                registered_lead_id = form_data.get("registered_lead_id")
                registered_lead_id = int(registered_lead_id)
                print(f"Registered user id is {registered_lead_id}")
                registered_lead = Leads.query.filter_by(
                    lead_id=registered_lead_id
                ).first()
                registered_lead.firstname = firstname
                registered_lead.lastname = lastname
                registered_lead.city = city
                registered_lead.phone = phone
                registered_lead.country = country
                registered_lead.industry = industry
                registered_lead.company = company
                registered_lead.persona = persona
                registered_lead.email = email
                registered_lead.group = group
                registered_lead.address = address
                registered_lead.description = description
                registered_lead.lead_status = lead_status
                registered_lead.lead_source = lead_source
                registered_lead.lead_title = lead_title
                registered_lead.lead_product = lead_product
                registered_lead.lead_owner = lead_owner
                registered_lead.update_lead_name()
                db.session.add(registered_lead)
                db.session.commit()
                print("User information updated")
                return True
        print("Failed adding new lead")
        return False
    except Exception as bug:
        print(bug)
        print("Failed adding new lead")
        return False


def load_all_leads(stage: str = None):
    try:
        all_leads = (
            Leads.query.all()
            if not stage
            else Leads.query.filter_by(lead_stage=stage).all()
        )
        if all_leads:
            return all_leads
        return []
    except Exception as bug:
        print(bug)
        return False


def get_latest_invoice_number():
    try:
        invoice_counter = InvoiceCounter.query.filter_by(invoice_id=1).first()
        if invoice_counter:
            invoice_counter.latest_invoice_number += 1
            db.session.add(invoice_counter)
            db.session.commit()
            return invoice_counter.latest_invoice_number
        else:
            new_invoice_counter = InvoiceCounter(latest_invoice_number=1)
            db.session.add(new_invoice_counter)
            db.session.commit()
            return 1
    except Exception as bug:
        print(bug)
        return 0


def generate_invoice_number():
    raw_invoice = "HCL-21-000000"
    latest_invoice_no = get_latest_invoice_number()
    invoice_len = len(str(latest_invoice_no))
    invoice_number = raw_invoice[:-invoice_len] + str(latest_invoice_no)
    return invoice_number


def add_deal_to_db(user_data: dict) -> bool:
    try:
        with app.app_context():
            if not user_data.get("is_account"):
                lead_id = int(user_data.get("lead_id"))
                deal_name = user_data.get("deal_name")
                closing_date = user_data.get("closing_date")
                deal_stage = user_data.get("deal_stage")
                contact_role = user_data.get("contact_role")
                closing_date = format_the_date(closing_date)
                containers, amount = create_container_order(user_data, True)
                lead = Leads.query.filter_by(lead_id=lead_id).first()
                if lead:
                    deal_company = (
                        lead.company
                        if lead.company
                        else f"{lead.firstname} {lead.lastname}"
                    )
                    new_deal = Deals(
                        deal_owner=flask_login.current_user.fullname,
                        deal_name=deal_name,
                        firstname=lead.firstname,
                        lastname=lead.lastname,
                        company=deal_company,
                        phone=lead.phone,
                        country=lead.country,
                        city=lead.city,
                        address=lead.address,
                        industry=lead.industry,
                        email=lead.email,
                        persona=lead.persona,
                        account_name=deal_company,
                        amount=amount,
                        containers=containers,
                        deal_stage=deal_stage,
                        closing_date=None,
                        invoice_number=generate_invoice_number(),
                        contact_role=contact_role,
                        no_container_types=len(json.loads(containers)),
                    )

                    new_account = Accounts(
                        account_name=new_deal.company,
                        firstname=new_deal.firstname,
                        lastname=new_deal.lastname,
                        company=new_deal.company,
                        phone=new_deal.phone,
                        country=new_deal.country,
                        city=new_deal.city,
                        address=new_deal.address,
                        email=new_deal.email,
                        persona=new_deal.persona,
                        source=lead.lead_source,
                        title=lead.lead_tile,
                        group=lead.group,
                        industry=new_deal.industry,
                        description=lead.description,
                        account_owner=flask_login.current_user.email,
                    )

                    new_crmcontact = CrmContacts(
                        account_name=new_deal.company,
                        firstname=new_deal.firstname,
                        lastname=new_deal.lastname,
                        company=new_deal.company,
                        phone=new_deal.phone,
                        country=new_deal.country,
                        city=new_deal.city,
                        address=new_deal.address,
                        email=new_deal.email,
                        persona=new_deal.persona,
                        contact_role=contact_role,
                        contact_owner=flask_login.current_user.email,
                    )
                    print(new_deal)
                    print(new_account)
                    print(new_crmcontact)
                    db.session.add(new_deal)
                    db.session.add(new_account)
                    db.session.add(new_crmcontact)
                    db.session.delete(lead)
                    db.session.commit()
                    return True
                print("Lead not found")
                return False
            else:
                account_id = int(user_data.get("account_id"))
                amount = user_data.get("amount")
                deal_name = user_data.get("deal_name")
                closing_date = user_data.get("closing_date")
                deal_stage = user_data.get("deal_stage")
                contact_role = user_data.get("contact_role")
                account = Accounts.query.filter_by(account_id=account_id).first()
                closing_date = format_the_date(closing_date)
                containers, amount = create_container_order(user_data, True)

                new_deal = Deals(
                    deal_owner=flask_login.current_user.email,
                    deal_name=account.account_name,
                    firstname=account.firstname,
                    lastname=account.lastname,
                    company=account.company,
                    phone=account.phone,
                    country=account.country,
                    city=account.city,
                    address=account.address,
                    industry=account.industry,
                    email=account.email,
                    persona=account.persona,
                    amount=amount,
                    containers=containers,
                    deal_stage=deal_stage,
                    contact_role=contact_role,
                    account_name=account.account_name,
                    closing_date=closing_date,
                    invoice_number=generate_invoice_number(),
                    no_container_types=len(json.loads(containers)),
                )

                db.session.add(new_deal)
                db.session.commit()
                return True
    except TypeError as bug:
        print(bug)
        print("damn damn")
        return False


def create_container_order(user_data: dict, return_total_amount=False) -> dict:
    try:
        order = {}
        total_container_types = int(user_data.get("total_rows"))
        total_amount = 0.0
        print(f"{total_container_types} found on the input")
        for container_type in range(1, total_container_types + 1):
            container_size = user_data.get(f"size_{container_type}")
            container_data = {
                "quantity": int(user_data.get(f"quantity_{container_type}")),
                "unit_price": float(user_data.get(f"price_{container_type}")),
            }
            order[container_size] = container_data
            total_amount += container_data["unit_price"] * container_data["quantity"]
        print(order)
        return (
            json.dumps(order)
            if not return_total_amount
            else (json.dumps(order), total_amount)
        )
    except Exception as bug:
        print(bug)
        print("Bug occured while creating container order")
        return json.dumps({})


def update_deal_info(status_data: dict) -> bool:
    try:
        with app.app_context():
            deal_id = status_data.get("deal_id")
            deal_stage = status_data.get("deal_stage")
            deal_end_date = status_data.get("deal_end_date")
            account_name = status_data.get("account_name")
            contact_role = status_data.get("contact_role")
            deal_id = int(deal_id)
            print(deal_end_date)

            containers, deal_amount = create_container_order(status_data, True)
            print(f"container {containers} Deal amount {deal_amount}")
            deal_end_date = format_the_date(deal_end_date)

            deal = Deals.query.filter_by(deal_id=deal_id).first()
            if deal:
                deal.deal_stage = deal_stage
                deal.amount = deal_amount
                deal.containers = containers
                deal.contact_role = contact_role
                deal.account_name = account_name
                deal.closing_date = deal_end_date
                deal.update_expected_revenue()
                db.session.add(deal)
                db.session.commit()
                print("Deal Information updated")
                return True
            print(f"Deal with Id of {deal_id} is not found on db")
            return False
    except Exception as bug:
        print(bug)
        print("Bug raised while updating deal information")
        return False


def load_all_deals(stage: str = None):
    try:
        all_deals = (
            Deals.query.all() if not stage else Deals.query.filter_by(deal_stage=stage)
        )
        if all_deals:
            return all_deals
        return []
    except Exception as bug:
        print(bug)
        return []


def update_accounts_info(account_data: dict) -> bool:
    try:
        with app.app_context():
            account_id = account_data.get("account_id")
            account_email = account_data.get("account_email")
            account_mobile = account_data.get("account_mobile")
            account_persona = account_data.get("account_persona")
            account_address = account_data.get("account_address")
            account_country = account_data.get("account_country")
            account_city = account_data.get("account_city")
            account_title = account_data.get("account_title")
            account_source = account_data.get("account_source")
            account_industry = account_data.get("account_industry")
            account_description = account_data.get("account_description")
            account_id = int(account_id)

            registered_account = Accounts.query.filter_by(account_id=account_id).first()
            print(registered_account)

            if registered_account:

                # =========Updating company information ==========
                registered_account.phone = account_mobile
                registered_account.address = account_address
                registered_account.email = account_email
                registered_account.country = account_country
                registered_account.city = account_city
                registered_account.persona = account_persona
                registered_account.title = account_title
                registered_account.source = account_source
                registered_account.industry = account_industry
                registered_account.description = account_description

                db.session.add(registered_account)
                db.session.commit()
                print("Account Information Updated")
                return True
            print("Account does not exist(update failed)")
            return False
    except Exception as bug:
        print(bug)
        print("Bug occured while updating account info")
        return False


def load_all_crm_accounts():
    try:
        all_crm_accounts = Accounts.query.all()
        return all_crm_accounts if all_crm_accounts else []
    except Exception as bug:
        print(bug)
        return []


def add_activity_todb(activity_data: dict) -> bool:
    try:
        with app.app_context():
            a_type = activity_data.get("a_type")
            a_time = activity_data.get("a_time")
            a_description = activity_data.get("a_description")
            a_account = f"{flask_login.current_user.firstname} {flask_login.current_user.lastname}"
            a_time = format_the_date(a_time)
            print(a_time)
            new_activity = Activities(
                a_type=a_type,
                a_time=a_time,
                a_owner=a_account,
                a_description=a_description,
                a_account=a_account,
                activity_owner=flask_login.current_user.email,
            )

            db.session.add(new_activity)
            db.session.commit()
            print("New activity added to db ")
            return True
    except Exception as bug:
        print(bug)
        print("bug occured while adding activity")
        return False


def load_all_activities():
    try:
        all_activities = Activities.query.all()
        return all_activities if all_activities else []
    except Exception as bug:
        print(bug)
        print("bug occured while loading activites")
        return []


def add_new_crm_contact(contact_data: dict) -> bool:
    try:
        with app.app_context():
            account_id = contact_data.get("account_id")
            firstname = contact_data.get("firstname")
            lastname = contact_data.get("lastname")
            email = contact_data.get("email")
            phone = contact_data.get("phone")
            contact_role = contact_data.get("contact_role")

            contact_account = Accounts.query.filter_by(account_id=account_id).first()
            if contact_account:
                new_crmcontact = CrmContacts(
                    user_id=flask_login.current_user.user_id,
                    firstname=firstname,
                    lastname=lastname,
                    email=email,
                    phone=phone,
                    account_name=contact_account.account_name,
                    company=contact_account.company,
                    contact_role=contact_role,
                    contact_owner=flask_login.current_user.email,
                )

                db.session.add(new_crmcontact)
                db.session.commit()
                print("new_crm_contact added")
                return True
            print("Contact is not related to any account")
            return False
    except Exception as bug:
        print(bug)
        print("Bug occured while adding new contact")
        return False


def load_all_crm_contacts():
    try:
        all_crm_contacts = CrmContacts.query.all()
        return all_crm_contacts if all_crm_contacts else []
    except Exception as bug:
        print(bug)
        print("Bug occured while loading crm contacts")
        return []


def get_proforma_containers(raw_containers: str) -> namedtuple:
    try:
        order_details = []
        container_data = json.loads(raw_containers)
        # print(container_data)
        for c_size in container_data:
            details = {
                "size": c_size,
                "quantity": container_data[c_size]["quantity"],
                "unit_price": container_data[c_size]["unit_price"],
                "total": container_data[c_size]["unit_price"]
                * container_data[c_size]["quantity"],
            }
            order_details.append(details)
        print(order_details)
        return order_details
    except Exception as bug:
        print(bug)
        return []


def get_profoma_details(deal_id: int) -> List:
    try:
        deal = Deals.query.filter_by(deal_id=deal_id).first()
        if deal:
            container_order = get_proforma_containers(deal.containers)
            return (deal, container_order)
        return []

    except Exception as bug:
        print(bug)
        return []


def process_setting_field(field: List) -> List:
    try:
        with app.app_context():
            print(f"Type {type(field)}")
            print(f"processing {field}")
            return json.dumps(
                [list(setting_field.values())[0] for setting_field in json.loads(field)]
            )

    except Exception as bug:
        print(bug)
        print("Bug raised while processing setting field")
        return []


def apply_crm_settings_change(setting_data: dict) -> bool:
    try:
        with app.app_context():
            print(setting_data)
            lead_sources = setting_data.get("lead_sources")
            lead_status = setting_data.get("lead_status")
            lead_industries = setting_data.get("lead_industries")
            lead_stages = setting_data.get("lead_stages")
            deal_types = setting_data.get("deal_types")
            lead_persona = setting_data.get("lead_persona")
            contact_roles = setting_data.get("contact_roles")
            activity_types = setting_data.get("activity_types")
            setting = CRM_Setting.query.filter_by(setting_id=1).first()
            if setting:
                if lead_sources:
                    setting.lead_sources = process_setting_field(lead_sources)
                if lead_status:
                    setting.lead_status = process_setting_field(lead_status)
                if lead_industries:
                    setting.lead_industries = process_setting_field(lead_industries)
                if lead_stages:
                    setting.lead_stages = process_setting_field(lead_stages)
                if deal_types:
                    setting.deal_types = process_setting_field(deal_types)
                if lead_persona:
                    setting.lead_persona = process_setting_field(lead_persona)
                if contact_roles:
                    setting.contact_roles = process_setting_field(contact_roles)
                if activity_types:
                    setting.activity_types = process_setting_field(activity_types)
                db.session.add(setting)
                db.session.commit()
                print("CRM Settings updated")
                return True

            new_crm_setting = CRM_Setting(
                lead_sources=process_setting_field(lead_sources),
                lead_status=process_setting_field(lead_status),
                lead_industries=process_setting_field(lead_industries),
                lead_stages=process_setting_field(lead_stages),
                deal_types=process_setting_field(deal_types),
                lead_persona=process_setting_field(lead_persona),
                contact_roles=process_setting_field(contact_roles),
                activity_types=process_setting_field(activity_types),
            )
            db.session.add(new_crm_setting)
            db.session.commit()
            return True

    except Exception as bug:
        print(bug)
        print("Bug thrown while updating settings")
        return False


def load_crm_settings() -> Union[List, CRM_Setting]:
    try:
        settings = CRM_Setting.query.filter_by(setting_id=1).first()
        if settings:
            print("returning settings")
            return settings
        print("no settings found")
        return []
    except Exception as bug:
        print(bug)
        print("Bug thrown while loading crm settings")


def generate_crm_summary() -> dict:
    try:
        c_user = flask_login.current_user
        if (
            c_user.is_admin
            or c_user.is_marketing
            or c_user.is_operation
            or c_user.is_accountant
        ):
            return {
                "lead_count": len(load_all_leads()),
                "deal_count": len(load_all_deals()),
                "account_count": len(load_all_crm_accounts()),
                "closed_won": len(Deals.query.filter_by(deal_stage="Closed Won").all()),
                "closed_lost": len(
                    Deals.query.filter_by(deal_stage="Closed Lost").all()
                ),
            }
        return {
            "lead_count": len(
                Leads.query.filter_by(lead_owner=flask_login.current_user.email).all()
            ),
            "deal_count": len(
                Deals.query.filter_by(deal_owner=flask_login.current_user.email).all()
            ),
            "account_count": len(
                Accounts.query.filter_by(
                    account_owner=flask_login.current_user.email
                ).all()
            ),
            "closed_won": len(Deals.query.filter_by(deal_stage="Closed Won").all()),
            "closed_lost": len(Deals.query.filter_by(deal_stage="Closed Lost").all()),
        }

    except Exception as bug:
        print(bug)
        print("Bug raised while generating lead summary")
        return {}


@crm_bp.route("/crm")
@crm_bp.route("/crm/leads", methods=["GET", "POST"])
@login_required
def crm():
    role = current_user_role()
    if role.can_view_lead:
        if request.method == "POST":
            if request.form.get("_method") == "put":
                add_leads_todb(request.form, update=True)
            else:
                print("adding new deal")
                add_leads_todb(request.form)
            return render_template(
                "crm.html",
                title="CRM | Leads",
                json=json,
                countries=get_all_countries(),
                role=current_user_role(),
                all_leads=load_all_leads(),
                crm_summary=generate_crm_summary(),
                default_fields=load_crm_settings(),
                d_leads=tobe_deleted_items("Lead"),
                campaigns=Campaign.unique_campaigns(),
            )
        else:
            return render_template(
                "crm.html",
                title="CRM | Leads",
                json=json,
                all_leads=load_all_leads(),
                role=current_user_role(),
                countries=get_all_countries(),
                crm_summary=generate_crm_summary(),
                default_fields=load_crm_settings(),
                d_leads=tobe_deleted_items("Lead"),
                campaigns=Campaign.unique_campaigns(),
            )

    if role.can_view_deal:
        return redirect(url_for("crm_bp.deals"))

    if role.can_view_crm_accounts:
        return redirect(url_for("crm_bp.accounts"))

    if role.can_view_crm_activity:
        return redirect(url_for("crm_bp.activities"))

    if role.can_view_crm_contact:
        return redirect(url_for("crm_bp.crm_contacts"))

    if role.can_view_crm_settings:
        return redirect(url_for("crm_bp.crm_settings"))

    else:
        return redirect(url_for("home_bp._401"))


@crm_bp.route("/crm/deals", methods=["GET", "POST"])
@login_required
def deals():
    if request.method == "POST":
        if request.form.get("_method") == "put":
            update_deal_info(request.form)
        else:
            add_deal_to_db(request.form)
        return render_template(
            "deals.html",
            title="Deals",
            role=current_user_role(),
            all_deals=load_all_deals(),
            json=json,
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )

    else:
        return render_template(
            "deals.html",
            title="Deals",
            role=current_user_role(),
            all_deals=load_all_deals(),
            json=json,
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )


@crm_bp.route("/crm/accounts", methods=["GET", "POST"])
@login_required
def accounts():
    print(load_all_crm_accounts())
    if request.method == "POST":
        if request.form.get("_method") == "put":
            update_accounts_info(request.form)

        elif request.form.get("_method") == "special_post":
            add_new_crm_contact(request.form)
        else:
            pass
        return render_template(
            "accounts.html",
            title="CRM | Accounts",
            role=current_user_role(),
            json=json,
            all_accounts=load_all_crm_accounts(),
            all_crm_contacts=load_all_crm_contacts(),
            all_deals=load_all_deals(),
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )
    else:
        return render_template(
            "accounts.html",
            title="CRM | Accounts",
            role=current_user_role(),
            json=json,
            all_accounts=load_all_crm_accounts(),
            all_crm_contacts=load_all_crm_contacts(),
            all_deals=load_all_deals(),
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )


@crm_bp.route("/crm/activities", methods=["GET", "POST"])
@login_required
def activities():
    if request.method == "POST":
        add_activity_todb(request.form)
        return render_template(
            "activities.html",
            title="CRM | Activities",
            role=current_user_role(),
            json=json,
            all_activities=load_all_activities(),
            default_fields=load_crm_settings(),
            crm_summary=generate_crm_summary(),
            accounts=load_all_crm_accounts(),
        )
    else:
        return render_template(
            "activities.html",
            title="CRM | Activities",
            role=current_user_role(),
            json=json,
            all_activities=load_all_activities(),
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
            accounts=load_all_crm_accounts(),
        )


@crm_bp.route("/crm/crm-contacts", methods=["GET", "POST"])
@login_required
def crm_contacts():
    if request.method == "POST":
        return render_template(
            "crm_contacts.html",
            title="CRM | Contacts",
            json=json,
            role=current_user_role(),
            all_crm_contacts=load_all_crm_contacts(),
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )
    else:
        return render_template(
            "crm_contacts.html",
            title="CRM | Contacts",
            role=current_user_role(),
            json=json,
            all_crm_contacts=load_all_crm_contacts(),
            crm_summary=generate_crm_summary(),
            default_fields=load_crm_settings(),
        )


@crm_bp.route("/crm/proforma/<deal_id>", methods=["GET"])
@login_required
def proforma(deal_id: int):
    deal_id = deal_id
    deal, container_order = get_profoma_details(deal_id)
    return render_template(
        "proforma.html",
        now=datetime.datetime.now(),
        settings=load_all_settings(),
        deal=deal,
        role=current_user_role(),
        json=json,
        float=float,
        int=int,
        all_container_orders=container_order,
        title="CRM | Pro Forma ",
        default_fields=load_crm_settings(),
    )


@crm_bp.route("/crm/crm-settings", methods=["GET", "POST"])
@login_required
def crm_settings():
    if request.method == "POST":
        if request.form:
            apply_crm_settings_change(request.form)
        return render_template(
            "crm_settings.html",
            title="CRM | Settings",
            role=current_user_role(),
            preset_settings=load_crm_settings(),
            json=json,
            crm_summary=generate_crm_summary(),
            campaigns=json.dumps(Campaign.unique_campaigns()),
        )
    else:
        return render_template(
            "crm_settings.html",
            title="CRM | Settings",
            role=current_user_role(),
            preset_settings=load_crm_settings(),
            json=json,
            crm_summary=generate_crm_summary(),
            campaigns=json.dumps(Campaign.unique_campaigns()),
        )


@crm_bp.route("/update-activity", methods=["GET", "POST"])
@login_required
def update_activity():
    _id = request.form.get("id")
    status = request.form.get("status")
    print(_id, status)
    if _id and status:
        _id = int(_id)
        active_activity = Activities.query.filter_by(a_id=_id).first()
        if active_activity:
            active_activity.a_status = status
            db.session.add(active_activity)
            db.session.commit()
            print("activity updated")
    return redirect(url_for("crm_bp.activities"))


@crm_bp.route("/crm/delete-lead", methods=["POST"])
@login_required
def delete_lead():
    current_email = flask_login.current_user.email
    lead_id = request.form.get("lead_id")
    reason = request.form.get("reason")
    if is_already_added("Lead", lead_id):
        return redirect(url_for("crm_bp.crm"))

    lead_to_delete = ItemsToDelete(
        item_id=lead_id, requested_by=current_email, reason=reason, table_name="Lead"
    )
    try:
        db.session.add(lead_to_delete)
        db.session.commit()
    except Exception as bug:
        print(bug)
    finally:
        return redirect(url_for("crm_bp.crm"))
