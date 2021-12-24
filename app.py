from flask import app
from erp.crm.crm import crm_settings
import os
import json
import datetime
from erp import create_app
from erp.models.harlos_db import db, Users, UserRoles, GeneralSetting, CRM_Setting

# import app


def initialize_db(config=False):
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
                lead_status=json.dumps(["Contacted", "Not contacted", "Future"]),
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

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)