from flask_login import login_required
from flask import Blueprint, render_template, url_for, redirect
from erp.models.harlos_db import (
    Accounts,
    Campaign,
    CustomerContacts,
    Leads,
    Deals,
    Container,
    Activities,
)

home_bp = Blueprint(
    "home_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def get_summary():
    return {
        "marketing_contact": len(CustomerContacts.query.all()),
        "campaigns": len(Campaign.query.all()),
        "customers": len(Accounts.query.filter_by(account_type="customer").all()),
        "leads": len(Leads.query.all()),
        "deals": len(Deals.query.all()),
        "activity": len(Activities.query.all()),
        "crm_accounts": len(Accounts.query.all()),
        "activities": Activities.query.all(),
        "stock": len(Container.query.all()),
        "stock_available": len(Container.query.filter_by(status="Available").all()),
        "stock_booked": len(Container.query.filter_by(status="Booked").all()),
        "stock_sold": len(Container.query.filter_by(status="Sold").all()),
    }


@home_bp.route("/", methods=["POST", "GET"])
@login_required
def index():
    return render_template("index.html", title="Dashboard", summary=get_summary())


@home_bp.route("/401")
@login_required
def _401():
    return render_template("401.html", title="Unauthorized")
