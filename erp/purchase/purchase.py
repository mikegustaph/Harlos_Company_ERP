import json
import flask_login
from flask import current_app as app
from flask_login import login_required
from erp.general import is_already_added, tobe_deleted_items
from erp.models.harlos_db import ItemsToDelete, Suppliers, db, UserRoles
from flask import Blueprint, url_for, redirect, render_template, request


purchase_bp = Blueprint(
    "purchase_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def format_the_price(value: str):
    if not isinstance(value, (int, float, str)):
        return None
    if isinstance(value, int):
        return float(value)
    if isinstance(value, str):
        value = value.replace(",", "")
        if value.isdigit():
            return float(value)
        return None


def add_new_supplier(supplier_data: dict) -> bool:
    try:
        with app.app_context():
            supplier_name = supplier_data.get("supplier_name")
            supplier_address = supplier_data.get("supplier_address")
            supplier_phone = supplier_data.get("supplier_phone")
            supplier_email = supplier_data.get("supplier_email")
            prev_credit_balance = supplier_data.get("prev_credit_balance")
            product_or_service = supplier_data.get("product_or_service")
            payment_details = supplier_data.get("payment_details")
            supplier_type = supplier_data.get("supplier_type")
            prev_credit_balance = format_the_price(prev_credit_balance)
            if supplier_data.get("update_request"):
                existing_supplier = Suppliers.query.filter_by(
                    name=supplier_name
                ).first()
                if supplier_name:
                    existing_supplier.name = supplier_name
                if supplier_address:
                    existing_supplier.address = supplier_address
                if supplier_phone:
                    existing_supplier.phone = supplier_phone
                if supplier_email:
                    existing_supplier.email = supplier_email
                if prev_credit_balance:
                    existing_supplier.prev_credit_balance = prev_credit_balance
                if product_or_service:
                    existing_supplier.product_or_service = product_or_service
                if payment_details:
                    existing_supplier.payment_details = payment_details
                if supplier_type:
                    existing_supplier.supplier_type = supplier_type
                db.session.add(existing_supplier)
                db.session.commit()
                print("Supplier/regulator details updated")
                return True

            new_supplier = Suppliers(
                name=supplier_name,
                address=supplier_address,
                phone=supplier_phone,
                email=supplier_email,
                prev_credit_balance=prev_credit_balance,
                product_or_service=product_or_service,
                payment_details=payment_details,
                supplier_type=supplier_type,
            )
            db.session.add(new_supplier)
            db.session.commit()
            print("SUpplier/Regulator details added")
            return True
    except Exception as bug:
        print(bug)
        print("Bug occured while adding new supplier")
        return False


def load_all_suppliers():
    try:
        return Suppliers.query.all() if Suppliers.query.all() else []
    except Exception as bug:
        print(bug)
        print("Bug occured while loading suppliers")
        return []


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get current role")
        print(bug)
        return None


@purchase_bp.route("/purchase", methods=["GET", "POST"])
@login_required
def purchase():
    current_user = get_current_role()
    if current_user.can_view_supplier:
        if request.method == "POST":
            if current_user.can_edit_supplier:
                add_new_supplier(request.form)
                return render_template(
                    "purchase.html",
                    title="Purchase",
                    suppliers=load_all_suppliers(),
                    role=get_current_role(),
                    d_suppliers=tobe_deleted_items("Suppliers"),
                )
            return redirect(url_for("home_bp._401"))
        else:
            return render_template(
                "purchase.html",
                title="Purchase",
                suppliers=load_all_suppliers(),
                role=get_current_role(),
                d_suppliers=tobe_deleted_items("Suppliers"),
            )
    return redirect(url_for("home_bp._401"))


@purchase_bp.route("/delete-supplier/", methods=["POST"])
def delete_supplier():
    current_email = flask_login.current_user.email
    supplier_id = request.form.get("supplier_id")
    reason = request.form.get("reason")
    if is_already_added("Suppliers", supplier_id):
        return redirect(url_for("purchase_bp.purchase"))

    try:
        deleted_supplier = ItemsToDelete(
            item_id=supplier_id,
            table_name="Suppliers",
            reason=reason,
            requested_by=current_email,
        )

        db.session.add(deleted_supplier)
        db.session.commit()
    except Exception as bug:
        print(bug)

    finally:
        return redirect(url_for("purchase_bp.purchase"))
