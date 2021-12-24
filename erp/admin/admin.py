import os
import flask_login
from erp.general import *
from erp import start_from_scratch
from collections import defaultdict
from flask import current_app as app
from flask_login import login_required
from typing import Container, List, Union, Any
from erp.crm.crm import current_user_role, format_the_date
from flask import Blueprint, url_for, redirect, render_template, request
from erp.models.harlos_db import (
    UserRoles,
    db,
    Users,
    ItemsToDelete,
    CustomerContacts,
    Leads,
    Suppliers,
)


admin_bp = Blueprint(
    "admin_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)

can = defaultdict(lambda: False)
can["on"] = True


def add_profile_image(profile_image, profile_email: str, is_signature=False) -> str:
    try:
        profile_path = "erp/static/img/users"
        p_image = profile_email.replace("@", "-")
        if not os.path.isdir(profile_path):
            os.mkdir(profile_path)
        user_profile_path = f"{profile_path}/{p_image}"
        if not os.path.isdir(user_profile_path):
            os.mkdir(user_profile_path)

        img_name = "profile.png" if not is_signature else "signature.png"
        img_full_path = os.path.join(user_profile_path, img_name)
        profile_image.save(img_full_path)
        print("Image saved successfully")
        return f"img/users/{p_image}/{img_name}"
    except Exception as bug:
        print(bug)
        print("Bug occured while adding profile image")
        return ""


def load_all_users() -> Union[Users, List]:
    try:
        return Users.query.all() if Users.query.all() else []
    except Exception as bug:
        print(bug)
        print("Bug raised while loading all users")
        return []


def update_marketing_roles(role_updates: dict, role_name: str) -> bool:
    try:
        with app.app_context():
            can_do_marketing = role_updates.get("can_do_marketing")
            can_view_marketing = role_updates.get("can_view_marketing")
            can_update_marketing = role_updates.get("can_update_marketing")
            can_delete_marketing = role_updates.get("can_delete_marketing")

            current_user_roles = UserRoles.query.filter_by(role_name=role_name).first()
            current_user_roles.can_do_marketing = can[can_do_marketing]
            current_user_roles.can_view_marketing = can[can_view_marketing]
            current_user_roles.can_update_marketing = can[can_update_marketing]
            current_user_roles.can_delete_marketing = can[can_delete_marketing]
            db.session.add(current_user_roles)
            db.session.commit()
            print("Marketing roles updated")
    except Exception as bug:
        print("Failed updating marketing roles")
        print(bug)
        return False


def update_crm_roles(role_updates: dict, role_name: str) -> bool:
    try:
        with app.app_context():

            current_user_role = UserRoles.query.filter_by(role_name=role_name).first()

            # ---------------Leads roles update -------------------
            can_add_lead = role_updates.get("can_add_lead")
            can_view_lead = role_updates.get("can_view_lead")
            can_edit_lead = role_updates.get("can_edit_lead")
            can_delete_lead = role_updates.get("can_delete_lead")

            current_user_role.can_add_lead = can[can_add_lead]
            current_user_role.can_view_lead = can[can_view_lead]
            current_user_role.can_edit_lead = can[can_edit_lead]
            current_user_role.can_delete_lead = can[can_delete_lead]

            # --------------Deals roles updates -------------------
            can_add_deal = role_updates.get("can_add_deal")
            can_view_deal = role_updates.get("can_view_deal")
            can_edit_deal = role_updates.get("can_edit_deal")
            can_delete_deal = role_updates.get("can_delete_deal")

            current_user_role.can_add_deal = can[can_add_deal]
            current_user_role.can_view_deal = can[can_view_deal]
            current_user_role.can_edit_deal = can[can_edit_deal]
            current_user_role.can_delete_deal = can[can_delete_deal]

            # ------------Crm accounts roles updates --------------
            can_add_crm_accounts = role_updates.get("can_add_crm_accounts")
            can_view_crm_accounts = role_updates.get("can_view_crm_accounts")
            can_edit_crm_accounts = role_updates.get("can_edit_crm_accounts")
            can_delete_crm_accounts = role_updates.get("can_delete_crm_accounts")

            current_user_role.can_add_crm_accounts = can[can_add_crm_accounts]
            current_user_role.can_view_crm_accounts = can[can_view_crm_accounts]
            current_user_role.can_edit_crm_accounts = can[can_edit_crm_accounts]
            current_user_role.can_delete_crm_accounts = can[can_delete_crm_accounts]

            # -------------Crm activity updates ---------------------
            can_create_crm_activity = role_updates.get("can_create_crm_activity")
            can_view_crm_activity = role_updates.get("can_view_crm_activity")
            can_edit_crm_activity = role_updates.get("can_edit_crm_activity")
            can_delete_crm_activity = role_updates.get("can_delete_crm_activity")

            current_user_role.can_create_crm_activity = can[can_create_crm_activity]
            current_user_role.can_view_crm_activity = can[can_view_crm_activity]
            current_user_role.can_edit_crm_activity = can[can_edit_crm_activity]
            current_user_role.can_delete_crm_activity = can[can_delete_crm_activity]

            # ------------Crm contacts roles updates --------------
            can_add_crm_contact = role_updates.get("can_add_crm_contact")
            can_view_crm_contact = role_updates.get("can_view_crm_contact")
            can_edit_crm_contact = role_updates.get("can_edit_crm_contact")
            can_delete_crm_contact = role_updates.get("can_delete_crm_contact")

            current_user_role.can_add_crm_contact = can[can_add_crm_contact]
            current_user_role.can_view_crm_contact = can[can_view_crm_contact]
            current_user_role.can_edit_crm_contact = can[can_edit_crm_contact]
            current_user_role.can_delete_crm_contact = can[can_delete_crm_contact]

            # ------------Crm settings roles updates --------------
            can_add_crm_settings = role_updates.get("can_add_crm_settings")
            can_view_crm_settings = role_updates.get("can_view_crm_settings")
            can_edit_crm_settings = role_updates.get("can_edit_crm_settings")
            can_delete_crm_settings = role_updates.get("can_delete_crm_settings")

            current_user_role.can_add_crm_settings = can[can_add_crm_settings]
            current_user_role.can_view_crm_settings = can[can_view_crm_settings]
            current_user_role.can_edit_crm_settings = can[can_edit_crm_settings]
            current_user_role.can_delete_crm_settings = can[can_delete_crm_settings]

            db.session.add(current_user_role)
            db.session.commit()
            print("CRM data updated")

    except Exception as bug:
        print("Failed to updated crm roles")
        print(bug)
        return False


def update_stock_roles(role_updates: dict, role_name: str):
    try:
        with app.app_context():

            current_user_role = UserRoles.query.filter_by(role_name=role_name).first()

            can_add_stock = role_updates.get("can_add_stock")
            can_view_stock = role_updates.get("can_view_stock")
            can_edit_stock = role_updates.get("can_edit_stock")
            can_delete_stock = role_updates.get("can_delete_stock")

            current_user_role.can_add_stock = can[can_add_stock]
            current_user_role.can_view_stock = can[can_view_stock]
            current_user_role.can_edit_stock = can[can_edit_stock]
            current_user_role.can_delete_stock = can[can_delete_stock]

            db.session.add(current_user_role)
            db.session.commit()
            print("Stock roles updated")
            return True
    except Exception as bug:
        print("Failed to update stock roles")
        print(bug)
        return False


def update_accounting_roles(role_updates: dict, role_name: str):
    try:
        with app.app_context():
            current_user_role = UserRoles.query.filter_by(role_name=role_name).first()

            can_do_accounting = role_updates.get("can_do_accounting")
            can_view_accounting = role_updates.get("can_view_accounting")
            can_edit_accounting = role_updates.get("can_update_accounting")
            can_delete_accounting = role_updates.get("can_delete_accounting")

            current_user_role.can_do_accounting = can[can_do_accounting]
            current_user_role.can_view_accounting = can[can_view_accounting]
            current_user_role.can_update_accounting = can[can_edit_accounting]
            current_user_role.can_delete_accounting = can[can_delete_accounting]

            db.session.add(current_user_role)
            db.session.commit()
            print("Accounting rolers updated")
            return True
    except Exception as bug:
        print("Failed to update accounting roles")
        print(bug)
        return False


def update_purchase_roles(role_updates: dict, role_name: str):
    try:
        with app.app_context():
            current_user_role = UserRoles.query.filter_by(role_name=role_name).first()

            can_add_supplier = role_updates.get("can_add_supplier")
            can_view_supplier = role_updates.get("can_view_supplier")
            can_edit_supplier = role_updates.get("can_edit_supplier")
            can_delete_supplier = role_updates.get("can_delete_supplier")

            current_user_role.can_add_supplier = can[can_add_supplier]
            current_user_role.can_view_supplier = can[can_view_supplier]
            current_user_role.can_edit_supplier = can[can_edit_supplier]
            current_user_role.can_delete_supplier = can[can_delete_supplier]

            db.session.add(current_user_role)
            db.session.commit()
            print("Purchase Roles updated")
            return True
    except Exception as bug:
        print("Failed to updated purchase roles")
        print(bug)
        return False


def update_form_roles(role_updates: dict, role_name: str) -> bool:
    try:
        with app.app_context():
            current_user_role = UserRoles.query.filter_by(role_name=role_name).first()

            # ------------------------CASH DEPOSIT FORM ------------------------------

            cash_deposit_form_create = role_updates.get("cash_deposit_form_create")
            cash_deposit_form_view = role_updates.get("cash_deposit_form_view")
            cash_deposit_form_edit = role_updates.get("cash_deposit_form_edit")
            cash_deposit_form_delete = role_updates.get("cash_deposit_form_delete")

            current_user_role.cash_deposit_form_create = can[cash_deposit_form_create]
            current_user_role.cash_deposit_form_view = can[cash_deposit_form_view]
            current_user_role.cash_deposit_form_edit = can[cash_deposit_form_edit]
            current_user_role.cash_deposit_form_delete = can[cash_deposit_form_delete]

            # -------------------- CASH REGISTER FORM -------------------------------

            cash_register_form_create = role_updates.get("cash_register_form_create")
            cash_register_form_view = role_updates.get("cash_register_form_view")
            cash_register_form_edit = role_updates.get("cash_register_form_edit")
            cash_register_form_delete = role_updates.get("cash_register_form_delete")

            current_user_role.cash_register_form_create = can[cash_register_form_create]
            current_user_role.cash_register_form_view = can[cash_register_form_view]
            current_user_role.cash_register_form_edit = can[cash_register_form_edit]
            current_user_role.cash_register_form_delete = can[cash_register_form_delete]

            # -------------------- CASH REQUISITION FORM ------------------------------

            cash_requisition_form_create = role_updates.get(
                "cash_requisition_form_create"
            )
            cash_requisition_form_view = role_updates.get("cash_requisition_form_view")
            cash_requisition_form_edit = role_updates.get("cash_requisition_form_edit")
            cash_requisition_form_delete = role_updates.get(
                "cash_requisition_form_delete"
            )

            current_user_role.cash_requisition_form_create = can[
                cash_requisition_form_create
            ]
            current_user_role.cash_requisition_form_view = can[
                cash_requisition_form_view
            ]
            current_user_role.cash_requisition_form_edit = can[
                cash_requisition_form_edit
            ]
            current_user_role.cash_requisition_form_delete = can[
                cash_requisition_form_delete
            ]

            # ---------------------CASH RETIREMENT FORM ---------------------------------

            cash_retirement_form_create = role_updates.get(
                "cash_retirement_form_create"
            )
            cash_retirement_form_view = role_updates.get("cash_retirement_form_view")
            cash_retirement_form_edit = role_updates.get("cash_retirement_form_edit")
            cash_retirement_form_delete = role_updates.get(
                "cash_retirement_form_delete"
            )

            current_user_role.cash_retirement_form_create = can[
                cash_retirement_form_create
            ]
            current_user_role.cash_retirement_form_view = can[cash_retirement_form_view]
            current_user_role.cash_retirement_form_edit = can[cash_retirement_form_edit]
            current_user_role.cash_retirement_form_delete = can[
                cash_retirement_form_delete
            ]

            # ------------------- -------CLAIM FORM -------------------------------------------

            claim_form_create = role_updates.get("claim_form_create")
            claim_form_view = role_updates.get("claim_form_view")
            claim_form_edit = role_updates.get("claim_form_edit")
            claim_form_delete = role_updates.get("claim_form_delete")

            current_user_role.claim_form_create = can[claim_form_create]
            current_user_role.claim_form_view = can[claim_form_view]
            current_user_role.claim_form_edit = can[claim_form_edit]
            current_user_role.claim_form_delete = can[claim_form_delete]

            # ---------------------- MATERIAL PURCHASE FORM --------------------------------

            material_purchase_form_create = role_updates.get(
                "material_purchase_form_create"
            )
            material_purchase_form_view = role_updates.get(
                "material_purchase_form_view"
            )
            material_purchase_form_edit = role_updates.get(
                "material_purchase_form_edit"
            )
            material_purchase_form_delete = role_updates.get(
                "material_purchase_form_delete"
            )

            current_user_role.material_purchase_form_create = can[
                material_purchase_form_create
            ]
            current_user_role.material_purchase_form_view = can[
                material_purchase_form_view
            ]
            current_user_role.material_purchase_form_edit = can[
                material_purchase_form_edit
            ]
            current_user_role.material_purchase_form_delete = can[
                material_purchase_form_delete
            ]

            # -------------------- MATERIAL REQUISITION FORM -----------------------------------

            material_requisition_form_create = role_updates.get(
                "material_requisition_form_create"
            )
            material_requisition_form_view = role_updates.get(
                "material_requisition_form_view"
            )
            material_requisition_form_edit = role_updates.get(
                "material_requisition_form_edit"
            )
            material_requisition_form_delete = role_updates.get(
                "material_requisition_form_delete"
            )

            current_user_role.material_requisition_form_create = can[
                material_requisition_form_create
            ]
            current_user_role.material_requisition_form_view = can[
                material_requisition_form_view
            ]
            current_user_role.material_requisition_form_edit = can[
                material_requisition_form_edit
            ]
            current_user_role.material_requisition_form_delete = can[
                material_requisition_form_delete
            ]

            # ------------------PAYMENT VOUCHER FORM -------------------------

            payment_voucher_form_create = role_updates.get(
                "payment_voucher_form_create"
            )
            payment_voucher_form_view = role_updates.get("payment_voucher_form_view")
            payment_voucher_form_edit = role_updates.get("payment_voucher_form_edit")
            payment_voucher_form_delete = role_updates.get(
                "payment_voucher_form_delete"
            )

            current_user_role.payment_voucher_form_create = can[
                payment_voucher_form_create
            ]
            current_user_role.payment_voucher_form_view = can[payment_voucher_form_view]
            current_user_role.payment_voucher_form_edit = can[payment_voucher_form_edit]
            current_user_role.payment_voucher_form_delete = can[
                payment_voucher_form_delete
            ]

            # ----------------- PETTY CASH RECONCILIATION FORM -------------------------------

            petty_cash_reconciliation_form_create = role_updates.get(
                "petty_cash_reconciliation_form_create"
            )
            petty_cash_reconciliation_form_view = role_updates.get(
                "petty_cash_reconciliation_form_view"
            )
            petty_cash_reconciliation_form_edit = role_updates.get(
                "petty_cash_reconciliation_form_edit"
            )
            petty_cash_reconciliation_form_delete = role_updates.get(
                "petty_cash_reconciliation_form_delete"
            )

            current_user_role.petty_cash_reconciliation_form_create = can[
                petty_cash_reconciliation_form_create
            ]
            current_user_role.petty_cash_reconciliation_form_view = can[
                petty_cash_reconciliation_form_view
            ]
            current_user_role.petty_cash_reconciliation_form_edit = can[
                petty_cash_reconciliation_form_edit
            ]
            current_user_role.petty_cash_reconciliation_form_delete = can[
                petty_cash_reconciliation_form_delete
            ]

            # ------------------ PETTY CASH VOUCHER FORM ------------------------

            petty_cash_voucher_form_create = role_updates.get(
                "petty_cash_voucher_form_create"
            )
            petty_cash_voucher_form_view = role_updates.get(
                "petty_cash_voucher_form_view"
            )
            petty_cash_voucher_form_edit = role_updates.get(
                "petty_cash_voucher_form_edit"
            )
            petty_cash_voucher_form_delete = role_updates.get(
                "petty_cash_voucher_form_delete"
            )

            current_user_role.petty_cash_voucher_form_create = can[
                petty_cash_voucher_form_create
            ]
            current_user_role.petty_cash_voucher_form_view = can[
                petty_cash_voucher_form_view
            ]
            current_user_role.petty_cash_voucher_form_edit = can[
                petty_cash_voucher_form_edit
            ]
            current_user_role.petty_cash_voucher_form_delete = can[
                petty_cash_voucher_form_delete
            ]

            # -------------- REFUND NOTE FORM ----------------------------------

            refund_note_form_create = role_updates.get("refund_note_form_create")
            refund_note_form_view = role_updates.get("refund_note_form_view")
            refund_note_form_edit = role_updates.get("refund_note_form_edit")
            refund_note_form_delete = role_updates.get("refund_note_form_delete")

            current_user_role.refund_note_form_create = can[refund_note_form_create]
            current_user_role.refund_note_form_view = can[refund_note_form_view]
            current_user_role.refund_note_form_edit = can[refund_note_form_edit]
            current_user_role.refund_note_form_delete = can[refund_note_form_delete]

            # ------------------STOCK ITEMS FORM ----------------------------------

            stock_items_create = role_updates.get("stock_items_create")
            stock_items_view = role_updates.get("stock_items_view")
            stock_items_edit = role_updates.get("stock_items_edit")
            stock_items_delete = role_updates.get("stock_items_delete")

            current_user_role.stock_items_create = can[stock_items_create]
            current_user_role.stock_items_view = can[stock_items_view]
            current_user_role.stock_items_edit = can[stock_items_edit]
            current_user_role.stock_items_delete = can[stock_items_delete]

            # ------------- SALES COMMISSION FORM ------------------------

            sales_commission_form_create = role_updates.get(
                "sales_commission_form_create"
            )
            sales_commission_form_view = role_updates.get("sales_commission_form_view")
            sales_commission_form_edit = role_updates.get("sales_commission_form_edit")
            sales_commission_form_delete = role_updates.get(
                "sales_commission_form_delete"
            )

            current_user_role.sales_commission_form_create = can[
                sales_commission_form_create
            ]
            current_user_role.sales_commission_form_view = can[
                sales_commission_form_view
            ]
            current_user_role.sales_commission_form_edit = can[
                sales_commission_form_edit
            ]
            current_user_role.sales_commission_form_delete = can[
                sales_commission_form_delete
            ]

            # -------------- QUOTATION FORM -------------------------------

            quotation_form_create = role_updates.get("quotation_form_create")
            quotation_form_view = role_updates.get("quotation_form_view")
            quotation_form_edit = role_updates.get("quotation_form_edit")
            quotation_form_delete = role_updates.get("quotation_form_delete")

            current_user_role.quotation_form_create = can[quotation_form_create]
            current_user_role.quotation_form_view = can[quotation_form_view]
            current_user_role.quotation_form_edit = can[quotation_form_edit]
            current_user_role.quotation_form_delete = can[quotation_form_delete]

            db.session.add(current_user_role)
            db.session.commit()
            print("User form roles updated")
            return True
        print("The app is running out of context")
    except Exception as bug:
        print("Failed to updated cash deposit form roles")
        print(bug)
        return False


@admin_bp.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            user_id = request.form.get("user_id")
            user_id = int(user_id) if user_id else 0
            print(f"User ID is {user_id}")
            update_details = request.form.get("update_user")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            gender = request.form.get("gender")
            date_of_birth = request.form.get("date_of_birth")
            email = request.form.get("email")
            user_password = request.form.get("password")
            _profile_image = request.files.get("profile_image")
            profile_signature = request.files.get("signature")
            user_type = request.form.get("user_type")
            status = request.form.get("user_status")
            role = request.form.get("role")

            date_of_birth = format_the_date(date_of_birth)
            profile_image = add_profile_image(_profile_image, email)
            profile_signature = add_profile_image(profile_signature, email, True)
            try:
                if update_details:
                    existing_user = Users.query.filter_by(user_id=user_id).first()
                    if existing_user:
                        print("Upgrading existing new user")
                        print(f"Birth date {date_of_birth}")
                        if firstname:
                            existing_user.new_firstname = firstname
                            print("username updated")
                        if lastname:
                            print("lastname updated")
                            existing_user.new_lastname = lastname
                        if gender:
                            print("gender updated")
                            existing_user.gender = gender
                        if email:
                            print("email updated")
                            existing_user.email = email
                        if date_of_birth:
                            print("date of birth updated")
                            existing_user.date_of_birth = date_of_birth
                        if profile_image.strip():
                            print("profile image updated")
                            existing_user.profile_image = profile_image
                        if user_password:
                            print("password updated")
                            existing_user.new_password = user_password
                        if profile_signature.strip():
                            print("signature updated")
                            existing_user.signature = profile_signature
                        if role:
                            print("role updated")
                            existing_user.role = role
                        if user_type:
                            existing_user.is_admin = (
                                True if user_type == "admin" else False
                            )
                        if status:
                            existing_user.is_active = (
                                True if status == "Active" else False
                            )

                        db.session.add(existing_user)
                        db.session.commit()
                else:
                    new_user = Users(
                        firstname=firstname,
                        lastname=lastname,
                        gender=gender,
                        email=email,
                        date_of_birth=date_of_birth,
                        profile_image=profile_image,
                        password=user_password,
                        signature=profile_signature,
                        role=role,
                        is_admin=True if user_type == "admin" else False,
                        is_active=True if status == "Active" else False,
                    )
                    print("Recording new user rule")
                    db.session.add(new_user)
                    db.session.commit()
                print("User data updated")
            except Exception as bug:
                print(bug)
                print("Bug occured while adding new user")
        return render_template("admin.html", title="Admin", users=load_all_users())
    return redirect(url_for("home_bp._401"))


@admin_bp.route("/actions", methods=["GET", "POST"])
@login_required
def actions():
    if flask_login.current_user.is_admin:
        delete_items = ItemsToDelete.query.all()
        if request.method == "POST":
            return render_template("actions.html", title="Admin", d_items=delete_items)
        return render_template("actions.html", title="Admin", d_items=delete_items)
    return redirect(url_for("home_bp._401"))


@admin_bp.route("/admin_activities", methods=["GET", "POST"])
@login_required
def admin_activities():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            return render_template("admin_activities.html", title="Admin")
        return render_template("admin_activities.html", title="Admin")
    return redirect(url_for("home_bp._401"))


@admin_bp.route("/roles", methods=["GET"])
@login_required
def roles():
    if flask_login.current_user.is_admin:
        return render_template("roles.html", title="Admin")
    return redirect(url_for("home_bp._401"))


@admin_bp.route("/roles_viewer/<role_name>", methods=["GET", "POST"])
@login_required
def roles_viewer(role_name: str):
    if flask_login.current_user.is_admin:
        role_type = UserRoles.query.filter_by(role_name=role_name).first()
        if request.method == "POST":
            print("Hell Yeah ", request.form.get("form_type"))
            if request.form.get("form_type") == "marketing":
                update_marketing_roles(request.form, role_name)
            elif request.form.get("form_type") == "crm":
                update_crm_roles(request.form, role_name)
            elif request.form.get("form_type") == "stock":
                update_stock_roles(request.form, role_name)
            elif request.form.get("form_type") == "purchase":
                update_purchase_roles(request.form, role_name)
            elif request.form.get("form_type") == "accounting":
                update_accounting_roles(request.form, role_name)
            elif request.form.get("form_type") == "form_roles":
                update_form_roles(request.form, role_name)
            else:
                pass
            return render_template(
                "roles_viewer.html", title="Admin", role_type=role_type
            )
        return render_template("roles_viewer.html", title="Admin", role_type=role_type)
    return redirect(url_for("home_bp._401"))


@admin_bp.route("/delete-everything", methods=["POST"])
@login_required
def delete_everything():
    current_user = flask_login.current_user
    if not current_user.is_admin:
        return redirect(url_for("admin_bp.admin"))
    start_from_scratch(app)
    return redirect(url_for("auth_bp.signin"))


@admin_bp.route("/delete-user/<int:user_id>")
@login_required
def delete_user(user_id):
    current_user = flask_login.current_user
    if not current_user.is_admin:
        return redirect(url_for("admin_bp.admin"))

    target_user = Users.query.filter_by(user_id=user_id).first()
    if not target_user or target_user.is_admin:
        return redirect(url_for("admin_bp.admin"))

    try:
        db.session.delete(target_user)
        db.session.commit()
    except Exception as bug:
        print(bug)
    finally:
        return redirect(url_for("admin_bp.admin"))


@admin_bp.route("/delete-item/<item>")
@login_required
def delete_item(item):
    current_user = flask_login.current_user
    if not current_user.is_admin or not isinstance(item, str):
        return redirect(url_for("admin_bp.actions"))
    try:
        table_name, item_id = item.split(":")
        item_id = int(item_id.strip())
        # Excute only when table is not form
        if table_db.get(table_name):
            target_table = table_db.get(table_name, None)
            target_item = target_table.query.get(item_id)
            d_item = ItemsToDelete.query.filter(
                (ItemsToDelete.table_name == table_name)
                & (ItemsToDelete.item_id == item_id)
            ).first()
            db.session.delete(d_item)
            db.session.delete(target_item)
            db.session.commit()

        # Excute only when a table is a from
        elif forms_db.get(table_name):
            target_table = forms_db.get(table_name, None)
            target_item = target_table.query.get(item_id)
            form_item = Forms.query.filter_by(reference=target_item.reference).first()
            d_item = ItemsToDelete.query.filter(
                (ItemsToDelete.table_name == table_name)
                & (ItemsToDelete.item_id == item_id)
            ).first()
            db.session.delete(target_item)
            db.session.delete(form_item)
            db.session.delete(d_item)
            db.session.commit()
        else:
            return redirect(url_for("admin_bp.actions"))

    except Exception as bug:
        print(bug)
        db.session.rollback()
    finally:
        return redirect(url_for("admin_bp.actions"))


@admin_bp.route("/ignore-delete/<item>")
def ignore_delete(item):
    current_user = flask_login.current_user
    if not (current_user.is_admin or current_user.role == "admnistrator"):
        return redirect(url_for("admin_bp.actions"))

    try:
        table_name, item_id = item.split(":")
        item_id = int(item_id.strip())
        target_item = ItemsToDelete.query.filter(
            (ItemsToDelete.table_name == table_name)
            & (ItemsToDelete.item_id == item_id)
        ).first()
        if target_item:
            db.session.delete(target_item)
            db.session.commit()
    except Exception as bug:
        print(bug)
    finally:
        return redirect(url_for("admin_bp.actions"))
