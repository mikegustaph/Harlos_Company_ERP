import flask_login
from random import choice
from flask_login import login_required
from erp.contacts.contact import Contact
from flask import Blueprint, render_template, url_for, redirect, request
from erp.general import is_already_added, tobe_deleted_items
from erp.models.harlos_db import (
    CustomerContacts,
    db,
    Users,
    UserRoles,
    Leads,
    ContactGroups,
    ItemsToDelete,
)

contacts_bp = Blueprint(
    "contacts_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

contact_book = Contact()


def load_all_groups():
    groups = ContactGroups.query.order_by(ContactGroups.date_created.desc()).all()
    return groups if groups else []


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get current role")
        print(bug)
        return None


def random_lead_owner():
    admin = Users.query.filter_by(is_admin=1).first()
    if admin:
        return admin.email
    return ""


@contacts_bp.route("/marketing/contacts", methods=["POST", "GET"])
@login_required
def contacts():
    if request.method == "POST":
        return render_template(
            "contacts.html",
            title="Marketing | Contacts",
            groups=load_all_groups(),
            to_delete_contacts=tobe_deleted_items("Marketing Contact"),
            all_contacts=contact_book.load_contacts("All"),
        )
    else:
        return render_template(
            "contacts.html",
            groups=load_all_groups(),
            title="Marketing | Contacts",
            to_delete_contacts=tobe_deleted_items("Marketing Contact"),
            all_contacts=contact_book.load_contacts("All"),
        )


@contacts_bp.route("/add-new-contacts", methods=["POST"])
@login_required
def add_new_contacts():
    current_role = get_current_role()
    if current_role.can_do_marketing:
        current_user = flask_login.current_user
        user_email = current_user.email
        filename = request.files.get("filepond")
        print(filename)
        if filename:
            contact_path = contact_book.save_contacts_to_file(filename)
            print(contact_path)
            print("{} added contacts".format(current_user))
            if not contact_book.add_contacts_to_db(contact_path, user_email):
                print("contacts not added")
            return redirect(url_for("contacts_bp.contacts"))
        print("no form found")
        return redirect(url_for("contacts_bp.contacts"))
    return redirect(url_for("home_bp._401"))


@contacts_bp.route("/add_contact_manually", methods=["POST"])
@login_required
def add_contact_manually():
    try:
        mobile = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")
        department = request.form.get("department")

        contact_exists = CustomerContacts.query.filter_by(mobile=mobile).first()
        if not contact_exists:
            new_contact = CustomerContacts(
                mobile=mobile,
                phone=mobile,
                email=email,
                address=address,
                department=department,
                added_by=flask_login.current_user.fullname,
                contact_owner=flask_login.current_user.email,
            )
            new_contact.new_group_name = "prospects"
            new_contact.set_contact_name = request.form.get("contact_name")
            db.session.add(new_contact)
            db.session.commit()
        return redirect(url_for("contacts_bp.contacts"))
    except Exception as bug:
        print(bug)
        return redirect(url_for("contacts_bp.contacts"))


@contacts_bp.route("/update_contact_group", methods=["POST"])
@login_required
def update_contact_group():
    current_role = get_current_role()
    if current_role.can_update_marketing:
        contact_id = request.form.get("contact_id")
        new_group_name = request.form.get("group_name")
        if new_group_name:
            target_contact = CustomerContacts.query.filter_by(
                contact_id=contact_id
            ).first()
            target_contact.new_group_name = new_group_name
            db.session.add(target_contact)
            db.session.commit()
            return redirect(url_for("contacts_bp.contacts"))
        print("Group name should not be empty")
        return redirect(url_for("contacts_bp.contacts"))
    return redirect(url_for("home_bp._401"))


@contacts_bp.route("/convert_to_lead/<contact_id>", methods=["GET"])
@login_required
def convert_to_lead(contact_id):
    current_user = get_current_role()
    if current_user.can_do_marketing:
        contact_id = int(contact_id) if contact_id.isdigit() else False
        if contact_id:
            prospect = CustomerContacts.query.filter_by(contact_id=contact_id).first()
            new_lead = Leads(
                firstname=prospect.firstname,
                lastname=prospect.lastname,
                city=prospect.mailing_city,
                phone=prospect.mobile,
                email=prospect.email,
                address=prospect.address,
                lead_owner=random_lead_owner(),
            )
            db.session.add(new_lead)
            db.session.delete(prospect)
            db.session.commit()
            print("Contact converted to lead")
            return redirect(url_for("contacts_bp.contacts"))
        print("Contact Id does not exist")
        return redirect(url_for("contacts_bp.contacts"))
    else:
        return redirect(url_for("home_bp._401"))


@contacts_bp.route("/delete-contact", methods=["POST"])
def delete_contact():
    current_email = flask_login.current_user.email
    contact_id = request.form.get("contact_id")
    reason = request.form.get("reason")
    if is_already_added("Marketing Contact", contact_id):
        return redirect("contacts_bp.contacts")

    try:
        contact_to_delete = ItemsToDelete(
            item_id=contact_id,
            table_name="Marketing Contact",
            reason=reason,
            requested_by=current_email,
        )
        db.session.add(contact_to_delete)
        db.session.commit()
    except Exception as bug:
        print(bug)

    finally:
        return redirect(url_for("contacts_bp.contacts"))
