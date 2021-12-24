import os
import csv
import time
from pathlib import Path
from typing import Union
from flask import current_app as app
from erp.models.harlos_db import db, Users, CustomerContacts


class Contact(object):
    def __init__(self):
        self.contact_path = "erp/contacts/contact-files"
        self.required_csv_fields = [
            "Account Name",
            "Email",
            "Phone",
            "Contact Owner",
            "Mobile",
            "Skype ID",
            "Mailing City",
            "Created By",
            "Created Time",
            "First Name",
            "Last Name",
            "Status",
            "Address",
            "Department",
        ]

    def load_contacts(self, status: Union[str, None] = None):
        try:
            with app.app_context():
                print(status)
                contacts = (
                    CustomerContacts.query.filter_by(group_name=status).all()
                    if status != "All"
                    else CustomerContacts.query.all()
                )
                if contacts:
                    return contacts
                return []
        except Exception as bug:
            print(bug)
            return []

    @property
    def contact_count(self, status: Union[str, None] = None):
        if not status:
            with app.app_context():
                return CustomerContacts.query.count()
        return CustomerContacts.query.filter_by(group_name=status)

    def load_customer_emails(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customers_with_email = []
            for customer in all_customer_contacts:
                if customer.email:
                    customers_with_email.append(customer)
            return customers_with_email
        except Exception as bug:
            print(bug)
            return

    def load_customer_phones(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customer_with_mobile = []
            for customer in all_customer_contacts:
                if customer.phone:
                    print(customer.phone)
                    customer_with_mobile.append(customer)
            return customer_with_mobile
        except Exception as bug:
            print(bug)
            return []

    def load_customer_twitter(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customers_with_twitter = []
            for customer in all_customer_contacts:
                if customer.twitter:
                    customers_with_twitter.append(customer)
            return customers_with_twitter
        except Exception as bug:
            print(bug)
            return

    def load_customer_linkedin(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customer_with_linkedin = []
            for customer in all_customer_contacts:
                if customer.linkedin:
                    customer_with_linkedin.append(customer)
            return customer_with_linkedin
        except Exception as bug:
            print(bug)
            return

    def load_customer_facebook(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customer_with_facebook = []
            for customer in all_customer_contacts:
                if customer.facebook:
                    customer_with_facebook.append(customer)
            return customer_with_facebook
        except Exception as bug:
            print(bug)
            return

    def load_customer_skype(self, status: Union[str, None] = None):
        try:
            all_customer_contacts = self.load_contacts(status=status)
            customer_with_skype = []
            for customer in all_customer_contacts:
                if customer.skype:
                    customer_with_skype.append(customer)
            return customer_with_skype
        except Exception as bug:
            print(bug)
            return

    def save_contacts_to_file(self, something) -> str:
        try:
            if not os.path.isdir(self.contact_path):
                os.mkdir(self.contact_path)
            filename = str(round(time.time())) + ".csv"
            contact_path = os.path.join(self.contact_path, filename)
            something.save(contact_path)
            return contact_path
        except Exception as bug:
            print(bug)
            return ""

    def make_new_user(self, user_data: dict) -> CustomerContacts:
        return CustomerContacts(
            firstname=user_data.get("firstname"),
            lastname=user_data.get("lastname"),
            mobile=user_data.get("mobile"),
            email=user_data.get("email"),
            twitter=user_data.get("twiiter"),
            facebook=user_data.get("facebook"),
            linkedin=user_data.get("linkedin"),
            phone=user_data.get("phone"),
            mailing_city=user_data.get("mail_city"),
            contact_owner=user_data.get("contact_owner"),
            added_by=user_data.get("added_by"),
            group_name=user_data.get("is_lead"),
            contact_name=user_data.get("account_name"),
            address=user_data.get("address"),
            department=user_data.get("department"),
        )

    def add_to_db(self, user_data: list) -> bool:
        try:
            with app.app_context():
                contact_exists = CustomerContacts.query.filter_by(
                    phone=user_data.get("phone")
                ).first()
                if not contact_exists:
                    print(user_data)
                    new_contact = self.make_new_user(user_data)
                    db.session.add(new_contact)
                    db.session.commit()
                    print("Contacts added to the db")
                return
        except Exception as bug:
            print(bug)
            return

    def get_column_index(self, header: list):
        field_indexes = {}
        for header_index in range(len(header)):
            if header[header_index] in self.required_csv_fields:
                field_indexes[header[header_index]] = header_index
        return field_indexes

    def add_contacts_to_db(
        self, filename: Union[Path, str], u_email: str = "somebody"
    ) -> bool:
        try:
            if os.path.isfile(filename):
                user_contacts = []
                with open(filename, "r") as customer_contacts:
                    _contacts = csv.reader(customer_contacts, delimiter=",")
                    header = next(_contacts)
                    print(header)
                    col_index = self.get_column_index(header)
                    print(self.get_column_index(header))
                    # firstname, lastname, mobile, email, twitter,
                    for row in _contacts:
                        print(row)
                        user_data = {}
                        user_data["firstname"] = (
                            row[col_index.get("First Name")]
                            if col_index.get("First Name")
                            else None
                        )
                        user_data["lastname"] = (
                            row[col_index.get("Last Name")]
                            if col_index.get("Last Name")
                            else None
                        )
                        user_data["mobile"] = (
                            row[col_index.get("Phone")]
                            if col_index.get("Phone")
                            else None
                        )
                        user_data["email"] = (
                            row[col_index.get("Email")]
                            if col_index.get("Email")
                            else None
                        )
                        user_data["twitter"] = (
                            row[col_index.get("Twitter")]
                            if col_index.get("Twitter")
                            else None
                        )
                        user_data["facebook"] = (
                            row[col_index.get("Facebook")]
                            if col_index.get("Facebook")
                            else None
                        )
                        user_data["linkedin"] = (
                            row[col_index.get("Linkedin")]
                            if col_index.get("Linkedin")
                            else None
                        )
                        user_data["mail_city"] = (
                            row[col_index.get("Mailing City")]
                            if col_index.get("Mailing City")
                            else None
                        )
                        user_data["account_name"] = (
                            row[col_index.get("Account Name")]
                            if col_index.get("Account Name")
                            else None
                        )

                        user_data["is_lead"] = (
                            row[col_index.get("Status")]
                            if col_index.get("Status")
                            else None
                        )

                        user_data["skype_id"] = (
                            row[col_index.get("Skype ID")]
                            if col_index.get("Skype ID")
                            else None
                        )

                        user_data["phone"] = (
                            row[col_index.get("Phone")]
                            if col_index.get("Phone")
                            else None
                        )

                        user_data["address"] = (
                            row[col_index.get("Address")]
                            if col_index.get("Address")
                            else None
                        )

                        user_data["department"] = (
                            row[col_index.get("Department")]
                            if col_index.get("Department")
                            else None
                        )
                        user_data["contact_owner"] = u_email

                        target_user = Users.query.filter_by(email=u_email).first()
                        user_data["added_by"] = (
                            target_user.fullname if target_user else None
                        )

                        if user_data.get("added_by"):
                            user_contacts.append(user_data)

                        print(user_data.get("is_lead"))
                        self.add_to_db(user_data=user_data)
                # print(user_contacts)
                print("all user data added")
                return True
            print("The path to the {} does not exist".format(filename))
            return
        except ValueError as bug:
            print(bug)
            print("exceptions thrown")
            return
