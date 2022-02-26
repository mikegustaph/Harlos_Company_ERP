import os
import json
import base64
import requests
import datetime
import flask_login
from flask import current_app as app
from collections import namedtuple
from flask_login import login_required
from erp.models.harlos_db import db, UserRoles, Deals, Container, GeneralSetting
from flask import Blueprint, url_for, redirect, render_template, request


accounting_bp = Blueprint(
    "accounting_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get current role")
        print(bug)
        return None


def load_all_deals(deal_id=None):
    if not deal_id:
        deals = Deals.query.all()
        for deal in deals:
            print(deal.attached_slip)
        if deals:
            return deals
        return []

    deal = Deals.query.filter_by(deal_id=deal_id).first()
    # print(f'This is deal : {deal}')
    if deal:
        return deal
    return []


def load_all_settings():
    settings = GeneralSetting.query.filter_by(setting_id=1).first()
    if settings:
        return settings
    return []


def get_proforma_containers(raw_containers: str) -> namedtuple:
    try:
        return json.loads(raw_containers)
    except Exception as bug:
        print(bug)
        return []


def save_payslip(invoice_number, invoice_data) -> str:
    try:
        root_path = "erp/static/img/invoice"
        payslip = invoice_data.get("payslip")
        invoice_number = invoice_number.replace("/", "-")

        if not os.path.isdir(root_path):
            os.mkdir(root_path)

        if not payslip:
            print("Invoice not attached")
            return ""

        payslip_path = f"{root_path}/{invoice_number}.pdf"
        payslip.save(payslip_path)
        return payslip_path
    except Exception as bug:
        print(bug)
        return ""


def send_invoice_to_web(
    order_number,
    path_to_invoice,
    url=f"{app.config['WEB_URL']}/account-receipt-attachment",
):
    """Loads an invoice and send it to eccomerce

    Args:
        order_number ([type]): [description]
        path ([type]): [description]
        url (str, optional): [description]. Defaults to ''.
    """
    try:
        binary_invoice = load_invoice_file(path_to_invoice)
        r_body = {"order-number": order_number, "binary-invoice": binary_invoice}

        response = requests.post(url, json=r_body)
        print(response.text)
    except Exception as bug:
        print(bug)
        print("Failed sending invoice to eccomerce")
        return


def load_invoice_file(path_to_invoice: str) -> str:
    """Returns encoded binary in base64

    Args:
        path_to_invoice (str): [description]

    Returns:
        str: [description]
    """
    try:
        with open(path_to_invoice, "rb") as invoice:
            binary_invoice = invoice.read()
        return base64.b64encode(binary_invoice)
    except Exception as bug:
        print(bug)
        print("Failed loading invoice from file")
        return


def update_stock_status(invoice_number: str) -> bool:
    """
        Will check if the deal being confirmed payment
        is attached to any container, if true it will update the
        container status to sold

    Args:
        invoice_number (str): invoice number of deal
    """

    target_container = Container.query.filter_by(invoice_number=invoice_number).first()
    if target_container:
        target_container.status = "Sold"
        target_container.payment_confirmed = True
        target_container.update_release_date()
        db.session.add(target_container)
        db.session.commit()
        return True
    return False


def approve_proforma_invoice(proforma: dict) -> bool:
    try:
        deal_id = proforma.get("deal_id")
        print(f"The deal id is {deal_id}")
        deal_id = int(deal_id) if deal_id.isdigit() else 0
        deal = Deals.query.filter_by(deal_id=deal_id).first()

        if not deal:
            print("deal does not exist")
            return False

        payslip = save_payslip(deal.invoice_number, request.files)

        if not payslip:
            print("payslip not attached")
            return False

        update_stock_status(deal.invoice_number)
        deal.approved_invoice = True
        deal.approved_by = flask_login.current_user.email
        deal.attached_invoice = payslip
        deal.deal_stage = "Closed Won"
        deal.update_expected_revenue()
        db.session.add(deal)
        db.session.commit()
        send_invoice_to_web(deal.invoice_number, deal.attached_invoice)
        print("The proforma have been approved successfully")

    except Exception as bug:
        print(bug)
        print("Failed approving proforma")
        return False


@accounting_bp.route("/accounting", methods=["GET", "POST"])
@login_required
def accounting():
    current_user = get_current_role()
    if current_user.can_view_accounting:
        if request.method == "POST":
            if current_user.can_update_accounting:
                print("Updating account")
                approve_proforma_invoice(request.form)
                return render_template(
                    "accounting.html",
                    title="Accounting",
                    settings=load_all_settings(),
                    deals=load_all_deals(),
                )
            return redirect(url_for("home_bp._401"))
        elif request.method == "GET":
            return render_template(
                "accounting.html",
                title="Accounting",
                settings=load_all_settings(),
                deals=load_all_deals(),
            )
    return redirect(url_for("home_bp._401"))


@accounting_bp.route("/accounting/<deal_id>")
@login_required
def account_proforma(deal_id):
    current_user = get_current_role()
    if current_user.can_view_accounting:
        deal_id = int(deal_id) if deal_id.isdigit() else 0
        deal = load_all_deals(deal_id)
        orders = get_proforma_containers(deal.containers) if deal else None
        return render_template(
            "invoice.html",
            title="Invoice",
            now=datetime.datetime.today(),
            settings=load_all_settings(),
            deal=deal,
            int=int,
            all_container_orders=orders,
        )
