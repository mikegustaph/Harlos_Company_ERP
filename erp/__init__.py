import os
import json
import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from erp.models.harlos_db import db, Users, UserRoles, GeneralSetting, CRM_Setting


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config.from_pyfile("config.py")
    migrate = Migrate()
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():

        from erp.auth.auth import auth_bp
        from erp.home.home import home_bp
        from erp.marketing.marketing import marketing_bp
        from erp.crm.crm import crm_bp
        from erp.stock.stock import stock_bp
        from erp.accounting.accounting import accounting_bp
        from erp.purchase.purchase import purchase_bp
        from erp.contacts.contacts import contacts_bp
        from erp.admin.admin import admin_bp
        from erp.settings.settings import settings_bp
        from erp.forms.forms import forms_bp
        from erp.profile.profile import profile_bp
        from erp.website.website import website_bp
        from erp.interface.interface import interface_bp

        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "auth_bp.signin"

        @login_manager.user_loader
        def user_loader(user_id):
            return Users.query.get(user_id)

        @app.context_processor
        def utility_processor():
            def get_user_role(user_id):
                role_name = Users.query.filter_by(user_id=user_id).first().role
                user_role = UserRoles.query.filter_by(
                    role_name=role_name).first()
                return user_role

            return dict(get_user_role=get_user_role)

        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(marketing_bp)
        app.register_blueprint(crm_bp)
        app.register_blueprint(stock_bp)
        app.register_blueprint(accounting_bp)
        app.register_blueprint(purchase_bp)
        app.register_blueprint(forms_bp)
        app.register_blueprint(contacts_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(settings_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(website_bp)
        app.register_blueprint(interface_bp)

    return app


def initialize_db(app, config=False):
    with app.app_context():
        if config:
            admin = Users(
                firstname="Loserian",
                lastname="Container",
                email="loserian@harlos.com",
                gender="Male",
                date_of_birth=datetime.datetime.utcnow(),
                profile_image="./static/img/users/default_profile.png",
                signature="./static/users/1/profile/signatature.jpg",
                password="Loserian@2016",
                role="administrator",
                is_admin=True,
            )

            default_settings = GeneralSetting(
                tax=18,
                currency="USD",
                name="Harlos Comp. Limited",
                email="info@harloscontainers.com",
                telephone="+255(0)22 286 2991/0767 118 847",
                address="Saza RD, New National Steel Building",
            )

            default_crm_settings = CRM_Setting(
                lead_sources=json.dumps(["media", "Tv", "SMS"]),
                lead_status=json.dumps(
                    ["Contacted", "Not contacted", "Future"]),
                lead_industries=json.dumps(["Matunda", "Bank", "Viwanda"]),
                lead_persona=json.dumps(["Money Oriented", "Alpha"]),
                contact_roles=json.dumps(["Developer", "Sales", "Manager"]),
                activity_types=json.dumps(["Phonecall", "Meeting"]),
            )

            # ============adding default accounts ============

            account_role = UserRoles(role_name="accountant")
            operation_role = UserRoles(role_name="operation")
            adminstrator_role = UserRoles(role_name="administrator")
            marketing_role = UserRoles(role_name="marketing")
            sales_role = UserRoles(role_name="sales")

            db.session.add(default_settings)
            db.session.add(default_crm_settings)

            db.session.add(account_role)
            db.session.add(operation_role)
            db.session.add(adminstrator_role)
            db.session.add(marketing_role)
            db.session.add(sales_role)

            db.session.add(admin)
            db.session.commit()

            print("Admin + Roles added")
        else:
            print("Inital config is inactive")


def start_from_scratch(app):
    print('Starting from scratch again')
    try:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            initialize_db(app, config=True)
    except Exception as bug:
        print(bug)
        print("Failed to start db from scratch")
