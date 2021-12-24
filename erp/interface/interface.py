import os
import json
import base64
import datetime
import re
from typing import Dict, List, Union
from erp.notification.notify import create_notification, make_notification
from flask import Blueprint, request, redirect, url_for, Response
from erp.models.harlos_db import Accounts, CrmContacts, db, Container, Leads, Deals
from erp.contacts.contacts import random_lead_owner
from erp.crm.crm import load_all_deals, load_all_leads, generate_invoice_number
from erp.website.website import load_customer_statistics, load_all_testimonials

interface_bp = Blueprint(
    "interface_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


@interface_bp.route("/interface")
def index():
    """Default route for interface

    Returns:
        json: To see if the JSON Interface is live
    """
    return {
        "testimonials": load_all_testimonials(as_json=True),
        "stats": load_customer_statistics(as_json=True),
    }


@interface_bp.route("/register_lead", methods=["POST"])
def register_lead():
    """Takes Customer sign up and register as lead to erp

    Returns:
        Response: (Message, status_code)
    """
    lead_data = request.get_json()
    response = add_leads_todb(lead_data)
    if response:
        return Response("Lead added successfully", 200)
    return Response("Failed adding lead", 502)


def add_leads_todb(lead_data: dict) -> bool:
    """Take leads data and add it to harlos-db

    Args:
        lead_data (dict): lead data from eccomerce sign up

    Returns:
        bool: Response of the action (True|False)
    """
    new_lead = Leads(
        firstname=lead_data.get("firstname"),
        lastname=lead_data.get("lastname"),
        phone=lead_data.get("phone"),
        email=lead_data.get("email"),
        address=lead_data.get("address"),
        lead_owner=random_lead_owner(),
    )

    try:
        db.session.add(new_lead)
        db.session.commit()
        title = "New Lead"
        message = f"{new_lead.lead_name} Registered on Eccomerce"
        make_deal_notification(title=title, message=message)
        return True
    except Exception as bug:
        print(bug)
        return False


@interface_bp.route("/interface/containers")
@interface_bp.route("/interface/containers/<number>")
def container_by_number(number: str = "all"):
    """Route for loading containers from erp -> ecommerce

    Args:
        number (str, optional): [container number]. Defaults to "all".

    Returns:
        [list]: [list of containers]
    """
    try:
        if number == "all":
            containers_list = []
            containers = Container.query.order_by(
                Container.date_created.desc()
            ).filter_by(status="Available")

            for _container in containers:
                if _container.visibility_on_website == 1:
                    containers_list.append(extract_container_data(_container))
            return json.dumps(containers_list)
        _container = Container.query.filter_by(number=number).first()
        return extract_container_data(_container)
    except Exception as bug:
        print(bug)
        return {}


def extract_container_data(_container) -> Dict:
    """Takes a container object and construct a json body

    Args:
        _container ([Containers]): [A containers objects]

    Returns:
        Dict: [Json|Dict formatted output]
    """
    try:
        if _container:
            print(_container.container_id)
            return {
                "id": _container.container_id,
                "number": _container.number,
                "status": _container.status,
                "size": _container.size,
                "general_condition": _container.general_condition,
                "conditions": _container.condition,
                "category": _container.category,
                "supplier": _container.supplier,
                "sale_price": _container.sale_price,
                "tax": _container.tax,
                "depot": _container.depot,
                "image": [
                    load_img_as_bytes(an_image)
                    for an_image in json.loads(_container.main_image)
                ],
            }
        return {}
    except Exception as bug:
        print(bug)
        print("Failed extracting computer-data")
        return {}


def load_img_as_bytes(path_to_img: str) -> str:
    """Load container image as butes

    Args:
        path_to_img (str): [a path to local stored container image]

    Returns:
        [str]: [base64 encoded bytestring of an image]
    """
    try:
        path_to_img = f"{os.getcwd()}/erp/static/{path_to_img}"
        with open(path_to_img, "rb") as image:
            content = image.read()
        return base64.encodebytes(content).decode("utf-8")
    except Exception as bug:
        print(os.getcwd())
        print(bug)
        print(f"cannot find path to {path_to_img}")
        return ""


@interface_bp.route("/update_expired_orders", methods=["POST"])
def update_expired_containers():
    """Update expired containers | Deals

    Returns:
        [Response]: [(Message, status_code)]
    """
    expired_orders = request.get_json()
    try:
        for container_number, invoice_number in expired_orders.items():
            container = Container.query.filter_by(number=container_number).first()
            deal = Deals.query.filter_by(invoice_number=invoice_number).first()
            if deal:
                container.status = "Available"
                deal.deal_stage = "Closed Lost"
                deal.update_expected_revenue()
                db.session.add(container)
                db.session.add(deal)
                db.session.commit()
        return Response("Container and Deals status updated successfully", 200)
    except Exception as bug:
        print(bug)
        print("Failed to update expired orders")
        return Response("Failed to update expired orders", 502)


@interface_bp.route("/register_deal", methods=["POST"])
def register_deal():
    """Route to Register new deal to erp

    Returns:
        [Response]: [(Message, status_code)]
    """
    deal_data = request.get_json()
    return add_deal_todb(deal_data)


def add_deal_todb(deal_data: dict) -> dict:
    """Add new deal to erp database

    Args:
        deal_data (dict): [deal-data recieved from ecommerce]

    Returns:
        dict: deal-data to construct eccomerce orders
    """
    deal_data["closing_date"] = iso_to_datetime(deal_data.get("closing_date"))
    user_email = deal_data.get("user_email")
    account = user_has_account(email=user_email)
    # print(account)
    if not account:
        user_lead = user_is_lead(user_email)
        # print(user_lead)
        if not user_lead:
            return Response("No Lead associated with this email", 502)

        invoice_number = register_deal_from_lead(user_lead, deal_data)
        print("Lead exist but bug occured")
        if invoice_number:
            make_deal_notification(user_lead.lead_name)
            return Response(json.dumps({"invoice_number": invoice_number}), 200)
        return Response(
            "Failed to register deal using lead, Internal server error", 502
        )
    print("Account Exist")
    invoice_number = register_deal_from_account(account, deal_data)
    if invoice_number:
        make_deal_notification(account.company)
        return Response(json.dumps({"invoice_number": invoice_number}), 200)
    return Response("Failed to register deal", 502)


def make_deal_notification(deal_name) -> None:
    make_notification(
        title="New Order Made",
        message=f"{deal_name} made new order from eccomerce",
    )


def user_has_account(email: str) -> Union[bool, Accounts]:
    """Checks whether an accounts with specified email exists

    Args:
        email (str): [email of the registered user]

    Returns:
        Union[bool, Accounts]: [Return Account if exist else Falses]
    """
    try:
        user_account = Accounts.query.filter_by(email=email).first()
        if user_account:
            return user_account
        return False
    except Exception as bug:
        print(bug)
        print("Failed getting user account")
        return False


def user_is_lead(email: str) -> Union[bool, Leads]:
    """Checks whether user has loading lead

    Args:
        email (str): [email of the registered user]

    Returns:
        Union[bool, Leads]: [Return Lead if exist else False]
    """
    try:
        lead = Leads.query.filter_by(email=email).first()
        if lead:
            return lead
        return False
    except Exception as bug:
        print(bug)
        print("Failed to checker whether user is lead | not")
        return False


def register_deal_from_account(account: Accounts, deal_data: dict) -> dict:
    """Register deal with an existing account to erp

    Args:
        account (Accounts): [account-name of the user]
        deal_data (dict): [deal-data from ecommerce]

    Returns:
        dict: [Response to construct ecommerce order]
    """
    deal_name = f"{account.firstname} {account.lastname}"
    new_deal = Deals(
        invoice_number=generate_invoice_number(),
        deal_owner=random_lead_owner(),
        deal_name=deal_name,
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
        dont_edit=True,
        amount=deal_data.get("amount"),
        containers=deal_data.get("containers"),
        deal_stage=deal_data.get("deal_stage"),
        contact_role=deal_data.get("contact_role"),
        account_name=account.account_name,
        closing_date=deal_data.get("closing_date"),
        no_container_types=deal_data.get("no_container_types"),
    )

    booked = book_container(
        deal=new_deal, container_number=deal_data.get("container_number")
    )
    if not booked:
        return False
    db.session.add(new_deal)
    db.session.add(booked)
    db.session.commit()
    print("Deal have have been registered successfully")
    return str(new_deal.invoice_number)


def register_deal_from_lead(lead: Leads, deal_data: dict) -> Union[bool, str]:
    """Returns invoice number of registered deal

    Args:
        lead_data (Leads): [Lead data of the registered user]
        deal_data (dict): [Deal data of the registered user]

    Returns:
        str: [Invoice number of the registered deal]
    """
    invoice_number = generate_invoice_number()
    deal_company = lead.company if lead.company else f"{lead.firstname} {lead.lastname}"

    new_deal = Deals(
        invoice_number=invoice_number,
        deal_owner=random_lead_owner(),
        deal_name=lead.lead_name,
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
        amount=deal_data.get("amount"),
        containers=deal_data.get("containers"),
        deal_stage=deal_data.get("deal_stage"),
        contact_role=deal_data.get("contact_role"),
        closing_date=deal_data.get("closing_date"),
        no_container_types=deal_data.get("no_container_types"),
    )

    try:
        booked = book_container(
            deal=new_deal, container_number=deal_data.get("container_number")
        )
        if not booked:
            return False
        new_account = add_new_account(new_deal)
        new_contact = add_new_crmContact(new_deal)
        db.session.add(new_deal)
        db.session.add(new_account)
        db.session.add(new_contact)
        db.session.delete(lead)
        db.session.add(booked)
        db.session.commit()
        print("New deal created from lead from ecommerce")
        return str(new_deal.invoice_number)
    except Exception as bug:
        print(bug)
        print("Failed to register deal from lead")
        return False


def add_new_account(new_deal: Deals) -> Accounts:
    """Register new user Account

    Args:
        new_deal (Deals): [new deal to be registered]

    Returns:
        Accounts: [new account to be registered]
    """
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
        account_owner=new_deal.deal_owner,
    )

    return new_account


def add_new_crmContact(new_deal: Deals) -> CrmContacts:
    """Register new Crm Contact

    Args:
        new_deal (Deals): [new deal to be registered]
        contact_role (str): [role of the contact in the company]

    Returns:
        CrmContacts: [CrmContacts belonging to an account]
    """

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
        contact_role=new_deal.contact_role,
        contact_owner=new_deal.deal_owner,
    )

    return new_crmcontact


def book_container(deal: Deals, container_number: str) -> bool:
    """Automatically book a container when order is placed

    Args:
        deal (Deals): [Deal booking the container]

    Returns:
        bool: [status of the booking whether (True|False)]
    """
    container_number = container_number.strip()
    target_container = Container.query.filter_by(number=container_number).first()
    if not target_container:
        print("Container you're trying to book does not exist")
        return False

    target_container.status = "Booked"
    target_container.invoice_number = deal.invoice_number
    return target_container


def iso_to_datetime(dt_str) -> datetime:
    """Take in Iso date string to python datetime

    Args:
        dt_str ([type]): [iso formatted date]

    Returns:
        [datetime]: [python datetime object]
    """
    try:
        dt, _, us = dt_str.partition(".")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us = int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)
    except Exception as bug:
        print(bug)
        print("Failed converting iso datetime to python datetime")
        return datetime.datetime.utcnow() + datetime.timedelta(days=3)


@interface_bp.route("/customer-payslip-attachment", methods=["POST"])
def customer_payslip_attachment():
    attachement_json = request.get_json()
    if not attachement_json:
        return {"response": "No attachement data sent"}
    return process_attachment(attachement_json)


def process_attachment(attachment_json: dict) -> bool:
    order_number = attachment_json.get("order-number")
    binary_pdf = attachment_json.get("binary-pdf")

    target_deal = Deals.query.filter_by(invoice_number=order_number).first()
    if not target_deal:
        response = {
            "response": "Order number send with pdf does not correspond to any deal"
        }
        return response

    payslip_path = save_payslip_to_file(binary_pdf, order_number)
    if not payslip_path:
        response = {
            "response": "Had trouble saving the attached pdf to file , please check again"
        }
        return response

    target_deal.attached_slip = payslip_path
    db.session.add(target_deal)
    db.session.commit()
    make_notification(
        title="Payslip Attachement",
        message=f"Customer with Deal name <{target_deal.deal_name}> attached payslip to payment",
    )
    print("Payslip Attached successfully")
    return {"response": "Payslip saved successfully to the erp "}


def save_payslip_to_file(binary_pdf: str, order_number: str) -> str:
    """Saves binary pdf to file

    Args:
        binary_pdf ([type]): [description]

    Returns:
        str: [description]
    """

    try:

        root_path = "erp/static/img/payslip"
        invoice_number = order_number.replace("/", "-")

        if not os.path.isdir(root_path):
            os.mkdir(root_path)

        payslip_path = f"{root_path}/{invoice_number}.pdf"
        decoded_binary = base64.b64decode(binary_pdf)
        with open(f"{payslip_path}", "wb") as payslip:
            payslip.write(decoded_binary)
        return payslip_path
    except Exception as bug:
        print(bug)
        print("Failed to save attached payslip to file")
        return
