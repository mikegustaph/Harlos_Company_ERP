import flask
import flask_login
from flask_login import login_required
from flask import current_app as app
from erp.models.harlos_db import db, GeneralSetting
from flask import Blueprint, url_for, redirect, render_template, request

settings_bp = Blueprint(
    "settings_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def save_organization_logo(img):
    try:
        path_to_img = "img/logo.png"
        new_logo_src = request.files.get("logo")
        img.save(new_logo_src)
        return path_to_img
    except Exception as bug:
        print("Failed to save a new organization logo")
        print(bug)
        return ""


def update_organization_settings(org_settings: dict):
    try:
        with app.app_context():
            organization_name = org_settings.get("organization_name")
            organization_telephone = org_settings.get("organization_telephone")
            organization_address = org_settings.get("organization_address")
            organization_email = org_settings.get("organization_email")
            # organization_logo = request.files.get("logo")
            # organization_logo = save_organization_logo(organization_logo)
            new_org_setting = GeneralSetting.query.filter_by(setting_id=1).first()

            if not new_org_setting:
                new_org_setting = GeneralSetting()

            new_org_setting.name = organization_name
            new_org_setting.email = organization_email
            new_org_setting.address = organization_address
            new_org_setting.telephone = organization_telephone

            db.session.add(new_org_setting)
            db.session.commit()
            print("Organization settings updated")
    except Exception as bug:
        print("Failed to update organization settings")
        print(bug)
        return False


def update_display_settings(display_settings: dict):
    try:
        with app.app_context():
            currency = display_settings.get("currency")
            tax = display_settings.get("tax")
            tax = int(tax.replace("%", ""))
            new_display_setting = GeneralSetting.query.filter_by(setting_id=1).first()
            if not display_settings:
                new_display_setting = GeneralSetting()
            new_display_setting.currency = currency
            new_display_setting.tax = tax
            db.session.add(new_display_setting)
            db.session.commit()
            print("Display setting updated")
    except Exception as bug:
        print("Failed to update display settings")
        print(bug)
        return False


def update_advanced_settings(org_settings: dict):
    try:
        pass
    except Exception as bug:
        print("Failed to update advanced settings")
        print(bug)
        return False


def load_all_settings():
    try:
        return GeneralSetting.query.filter_by(setting_id=1).first()
    except Exception as bug:
        print("Failed to load all settings")
        print(bug)
        return []


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            update_organization_settings(request.form)
        return render_template(
            "settings.html", title="Settings", settings=load_all_settings()
        )
    return redirect(url_for("home_bp._401"))


@settings_bp.route("/display", methods=["GET", "POST"])
@login_required
def display():
    if flask_login.current_user.is_admin:
        if request.method == "POST":
            update_display_settings(request.form)
        return render_template(
            "display.html", title="Settings", settings=load_all_settings()
        )
    return redirect(url_for("home_bp._401"))


@settings_bp.route("/advanced", methods=["GET", "POST"])
@login_required
def advanced():
    if flask_login.current_user.is_admin:
        return render_template(
            "advanced.html", title="Settings", settings=load_all_settings()
        )
    return redirect(url_for("home_bp._401"))
