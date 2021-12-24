import os
import time
import json
import typing
import datetime
import flask_login
from PIL import Image
from typing import Any
from flask.helpers import total_seconds
from flask_login import login_required
from flask import current_app as app
from erp.crm.crm import format_the_date
from erp.purchase.purchase import load_all_suppliers
from erp.general import is_already_added, tobe_deleted_items
from flask import Blueprint, url_for, redirect, render_template, request
from erp.models.harlos_db import (
    Container,
    ItemsToDelete,
    db,
    Stock,
    Suppliers,
    UserRoles,
    Deals,
)


stock_bp = Blueprint(
    "stock_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def format_the_price(raw_price: str) -> float:
    try:
        return int(float(raw_price.replace(",", ""))) if raw_price else 0
    except Exception as bug:
        print(bug)
        print("Failed to format the price")
        return 0


def load_approved_invoices():
    try:
        approved_invoices = (
            Deals.query.order_by(Deals.date_created.desc())
            .filter_by(approved_invoice=True)
            .all()
        )

        if approved_invoices:
            return approved_invoices
        return []
    except Exception as bug:
        print(bug)
        return []


def generate_stock_summary():
    try:
        with app.app_context():
            return {
                "available": len(Container.query.filter_by(status="Available").all()),
                "booked": len(Container.query.filter_by(status="Booked").all()),
                "on_hold": len(Container.query.filter_by(status="On Hold").all()),
                "outwards": len(Container.query.filter_by(status="Outwards").all()),
                "sold": len(Container.query.filter_by(status="sold").all()),
            }
    except Exception as bug:
        print(bug)
        print("Bug ocuured while updating stock")
        return {"available": 0, "booked": 0, "sold": 0}


def save_outward_order_invoice(order_invoice_img: Any, container_number: str) -> bool:
    try:
        container_path = f"erp/static/img/containers/{container_number}/invoice.pdf"
        order_invoice_img.save(container_path)
        return f"img/containers/{container_number}/invoice.pdf"
    except Exception as bug:
        print(bug)
        print("Bug thrown while saving outward order invoice")
        return False


def update_container_status(container_data: dict) -> bool:
    try:
        with app.app_context():
            container_id = container_data.get("container_id")
            new_status = container_data.get("status")
            active_container = Container.query.filter_by(
                container_id=container_id
            ).first()
            if active_container:
                if new_status == "Available" or new_status == "On Hold":
                    on_hold_reason = container_data.get("on_hold_reason")

                    active_container.status = new_status
                    active_container.on_hold_reason = on_hold_reason

                    # ----------emptying the rest ------------
                    active_container.truck_no = ""
                    active_container.outward_no = ""
                    active_container.driver_name = ""
                    active_container.driver_license = ""
                    active_container.invoice_number = ""

                elif new_status == "Outwards":
                    truck_no = container_data.get("truck_number")
                    driver_name = container_data.get("driver_name")
                    outward_no = container_data.get("outward_number")
                    order_invoice = request.files.get("order_invoice")
                    driver_license = container_data.get("driver_license")
                    order_invoice = save_outward_order_invoice(
                        order_invoice, active_container.number
                    )
                    active_container.status = new_status
                    active_container.truck_no = truck_no
                    active_container.outward_no = outward_no
                    active_container.driver_name = driver_name
                    active_container.order_invoice = order_invoice
                    active_container.driver_license = driver_license
                    active_container.update_release_date()

                    # --------emptying booked details -----------------
                    active_container.invoice_number = ""
                    active_container.on_hold_reason = ""

                elif new_status == "Booked":
                    invoice_number = container_data.get("invoice_number")
                    active_container.status = new_status
                    active_container.invoice_number = invoice_number

                    # -----------emptying outward details-----------
                    active_container.truck_no = ""
                    active_container.outward_no = ""
                    active_container.driver_name = ""
                    active_container.driver_license = ""
                    active_container.on_hold_reason = ""

                else:
                    print(f"{new_status} is impossible status")
                db.session.add(active_container)
                db.session.commit()
                print("Container status updated")
                return True
            print("No active container found, Please check your container name")
    except Exception as bug:
        print(bug)
        print("Bug occured while updating container status")
        return False


def get_container_pictures(container_number: str) -> str:
    pictures = []
    try:
        with app.app_context():
            attachments = request.files
            for key, item in attachments.items():
                saved_image = save_container_image(item, container_number)
                pictures.append(saved_image)
        return json.dumps(pictures)
    except Exception as bug:
        print(bug)
        return json.dumps(pictures)


def timestamp_string():
    return str(time.time())


def save_container_image(container_img: Any, container_number: str) -> str:
    try:
        container_path = "erp/static/img/containers"
        if not os.path.isdir(container_path):
            os.mkdir(container_path)
        image_dir = f"{container_path}/{container_number}"
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        suffix = f"{timestamp_string()}.png"
        image_name = f"{image_dir}/{suffix}"
        _container_img = Image.open(container_img).resize(
            (400, 350), resample=Image.LANCZOS
        )
        _container_img.save(image_name, quality = 3)

        return f"img/containers/{container_number}/{suffix}"
    except Exception as bug:
        print(bug)
        print("Bug thrown while saving container image")
        return ""


def add_new_stock(stock_data: dict) -> bool:
    try:
        with app.app_context():
            container_number = stock_data.get("container_number")
            stock_in_date = stock_data.get("stock_in_date")
            purchase_price = stock_data.get("purchase_price")
            sale_price = stock_data.get("sale_price")
            category = stock_data.get("category")
            size = stock_data.get("size")
            tax = stock_data.get("tax")
            status = stock_data.get("status")
            depot = stock_data.get("depot")
            supplier = stock_data.get("supplier")
            outward_no = stock_data.get("outward_no")
            condition = stock_data.get("condition")
            general_condition = stock_data.get("general_condition")
            main_image = request.files.get("main_image")
            website_visibility = stock_data.get("visible_on_website")
            tax = int(tax) if tax else None
            general_condition = (
                general_condition.capitalize()
                if general_condition
                else general_condition
            )
            condition = extract_condition_data(condition)
            sale_price = format_the_price(sale_price)
            purchase_price = format_the_price(purchase_price)
            website_visibility = True if website_visibility == "Yes" else False
            main_image = get_container_pictures(container_number)
            stock_in_date = format_the_date(stock_in_date) if stock_in_date else None

            new_stock = Container(
                number=container_number,
                status=status,
                size=size,
                condition=condition,
                category=category,
                supplier=supplier,
                purchase_price=purchase_price,
                sale_price=sale_price,
                tax=tax,
                depot=depot,
                outward_no=outward_no,
                main_image=main_image,
                general_condition=general_condition,
                visibility_on_website=website_visibility,
                stock_in_date=stock_in_date,
            )

            db.session.add(new_stock)
            db.session.commit()
            print("New stock Successfully added")
            return True
    except Exception as bug:
        print(bug)
        print("Bug raised when adding new stock")
        return False


def extract_condition_data(conditions: str) -> list:
    try:
        print(conditions)
        if isinstance(conditions, str):
            conditions = conditions.split(",")
            conditions = [condition.strip() for condition in conditions]
            return json.dumps(conditions)
        return "[]"
    except Exception as bug:
        print(bug)
        print("Bug raised while extracting container data")
        return "[]"


def update_container_details(stock_data: dict) -> bool:
    try:
        _id = stock_data.get("_id")
        purchase_price = stock_data.get("purchase_price")
        sale_price = stock_data.get("sale_price")
        category = stock_data.get("category")
        size = stock_data.get("size")
        depot = stock_data.get("depot")
        supplier = stock_data.get("supplier")
        condition = stock_data.get("condition")
        general_condition = stock_data.get("general_condition")
        website_visibility = stock_data.get("visible_on_website")
        stock_out_date = format_the_date(stock_data.get("stock_out_date"))
        print(type(condition))
        _id = int(_id) if _id else None
        condition = extract_condition_data(condition)
        print(f"Condition: {condition}")
        sale_price = format_the_price(sale_price)
        purchase_price = format_the_price(purchase_price)
        website_visibility = True if website_visibility == "Yes" else False

        if not _id:
            print("Container id could not be found")
            return False

        container = Container.query.filter_by(container_id=_id).first()

        if not container:
            print("Container does not exist")
            return False
        if supplier:
            container.supplier = supplier
        if purchase_price:
            container.purchase_price = purchase_price
        if sale_price:
            container.sale_price = sale_price
        if category:
            container.category = category
        if size:
            container.size = size
        if depot:
            container.depot = depot
        if general_condition:
            container.general_condition = general_condition.capitalize()
        if stock_out_date:
            container.release_date = datetime.datetime.fromordinal(
                stock_out_date.toordinal()
            )

        container.visibility_on_website = website_visibility

        db.session.add(container)
        db.session.commit()
        print("Container details updated")
        return True
    except Exception as bug:
        print(bug)
        print("Failed updating container details")
        return False


def all_condition_viewable():
    try:
        return [
            "Dent",
            "Rusty",
            "Pushed Out",
            "Pushed In",
            "Hole",
            "Patches",
            "Floor Deformed",
            "Door Problem",
            "Normal",
            "Good",
            "Very Good",
            "Cut",
            "Not inspected",
        ]

    except Exception as bug:
        print(bug)
        print("Failed constructing viewable condition")
        return []


def load_all_stocks():
    try:
        return Container.query.all() if Container.query.all() else []
    except Exception as bug:
        print(bug)
        print("Bug raised while loading all stocks")
        return []


def load_all_deals():
    try:
        deals = Deals.query.all()
        if deals:
            return deals
        return []
    except Exception as bug:
        print("Failed to load all deals")
        print(bug)
        return []


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get current role")
        print(bug)
        return None


@stock_bp.route("/stock", methods=["GET", "POST"])
@login_required
def stock():
    current_user = get_current_role()
    if current_user.can_view_stock:
        if request.method == "POST":
            if current_user.can_edit_stock:
                if request.form.get("_method") == "put":
                    update_container_status(request.form)
                elif request.form.get("_method") == "update_container_details":
                    update_container_details(request.form)
                else:
                    add_new_stock(request.form)
                return render_template(
                    "stock.html",
                    title="Stock | Containers",
                    json=json,
                    all_conditions=all_condition_viewable(),
                    deals=load_all_deals(),
                    invoices=load_approved_invoices(),
                    suppliers=load_all_suppliers(),
                    stocks=load_all_stocks(),
                    stock_summary=generate_stock_summary(),
                    role=get_current_role(),
                    d_stocks=tobe_deleted_items("Stock"),
                )

            return redirect(url_for("home_bp._401"))
        else:
            return render_template(
                "stock.html",
                title="Stock | Containers",
                json=json,
                deals=load_all_deals(),
                all_conditions=all_condition_viewable(),
                invoices=load_approved_invoices(),
                suppliers=load_all_suppliers(),
                stocks=load_all_stocks(),
                stock_summary=generate_stock_summary(),
                role=get_current_role(),
                d_stocks=tobe_deleted_items("Stock"),
            )
    return redirect(url_for("home_bp._401"))


@stock_bp.route("/release-orders", methods=["GET", "POST"])
@login_required
def release_orders():
    if flask_login.current_user.is_admin:
        return render_template(
            "release-orders.html",
            title="Release Orders",
            stock_summary=generate_stock_summary(),
            role=get_current_role(),
            all_containers=load_all_stocks(),
            invoices=load_approved_invoices(),
        )
    return redirect(url_for("home_bp._401"))


@stock_bp.route("/release-order/<c_number>", methods=["GET", "POST"])
@login_required
def release_order(c_number):
    if flask_login.current_user.is_admin:
        print(c_number)
        target_container = Container.query.filter_by(number=c_number).first()
        print(target_container)
        return render_template(
            "release-order.html",
            title="Release Orders",
            role=get_current_role(),
            target_container=target_container,
        )
    return redirect(url_for("home_bp._401"))


@stock_bp.route("/delete-container", methods=["POST"])
def delete_container():
    current_email = flask_login.current_user.email
    container_id = request.form.get("container_id")
    reason = request.form.get("reason")
    if is_already_added("Stock", container_id):
        return redirect(url_for("stock_bp.stock"))

    try:
        deleted_container = ItemsToDelete(
            item_id=container_id,
            table_name="Stock",
            reason=reason,
            requested_by=current_email,
        )
        db.session.add(deleted_container)
        db.session.commit()
        print("Container added to delete list")
    except Exception as bug:
        print(bug)
    finally:
        return redirect(url_for("stock_bp.stock"))
