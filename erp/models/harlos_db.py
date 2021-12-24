import json
import hashlib
import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})


class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=True)
    fullname = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=True)
    signature = db.Column(db.String(300), nullable=True)
    profile_image = db.Column(db.String(300), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(100), default="Not assigned")
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # ======================================================
    # ============== ROLES OF USERS ========================
    # ======================================================

    is_accountant = db.Column(db.Boolean, default=False)
    is_administrator = db.Column(db.Boolean, default=False)
    is_operation = db.Column(db.Boolean, default=False)
    is_sales = db.Column(db.Boolean, default=False)
    is_marketing = db.Column(db.Boolean, default=False)

    date_created = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.password = hashlib.sha256(self.password.encode()).hexdigest()
        self.fullname = f"{self.firstname} {self.lastname}"
        role = self.role.lower()
        self.set_role(role)

    def set_role(self, role):
        if role == "accountant":
            print("Accountant added")
            self.is_accountant = True
            self.is_administrator = False
            self.is_operation = False
            self.is_marketing = False
            self.is_sales = False
        elif role == "administrator":
            print("administrator added")
            self.is_accountant = False
            self.is_administrator = True
            self.is_operation = False
            self.is_marketing = False
            self.is_sales = False
        elif role == "operation":
            print("operation added")
            self.is_accountant = False
            self.is_administrator = False
            self.is_operation = True
            self.is_marketing = False
            self.is_sales = False
        elif role == "marketing":
            print("marketing added")
            self.is_accountant = False
            self.is_administrator = False
            self.is_operation = False
            self.is_marketing = True
            self.is_sales = False

        elif role == "sales":
            print("sales added")
            self.is_accountant = False
            self.is_administrator = False
            self.is_operation = False
            self.is_marketing = False
            self.is_sales = True
        else:
            print("role not specified")
            self.is_accountant = False
            self.is_administrator = False
            self.is_operation = False
            self.is_marketing = False
            self.is_sales = False

    @property
    def new_password(self):
        return self.password

    @property
    def new_firstname(self):
        return self.firstname

    @property
    def new_lastname(self):
        return self.lastname

    @new_firstname.setter
    def new_firstname(self, new_firstname):
        self.firstname = new_firstname
        self.fullname = f"{self.new_firstname} {self.lastname}"

    @new_lastname.setter
    def new_lastname(self, new_lastname):
        self.lastname = new_lastname
        self.fullname = f"{self.firstname} {self.new_lastname}"

    @new_password.setter
    def new_password(self, new_password):
        self.password = hashlib.sha256(new_password.encode()).hexdigest()

    def is_authorised(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password

    def __str__(self):
        return f"<User> {self.firstname}"

    def __repr__(self):
        return f"<User> {self.firstname}"

    def get_id(self):
        return f"{self.user_id}"


class UserRoles(db.Model):
    __tablename__ = "useroles"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(120), nullable=False)

    # --------------------DASHBOARD --------------------------

    can_view_dashboard = db.Column(db.Boolean, default=False)
    can_edit_dashboard = db.Column(db.Boolean, default=False)
    can_delete_dashboard = db.Column(db.Boolean, default=False)

    # -----------------MARKETING -----------------------------

    can_do_marketing = db.Column(db.Boolean, default=False)
    can_view_marketing = db.Column(db.Boolean, default=False)
    can_update_marketing = db.Column(db.Boolean, default=False)
    can_delete_marketing = db.Column(db.Boolean, default=False)

    # -------------- ACCOUNTANT MODULE ----------------------------
    can_do_accounting = db.Column(db.Boolean, default=False)
    can_view_accounting = db.Column(db.Boolean, default=False)
    can_update_accounting = db.Column(db.Boolean, default=False)
    can_delete_accounting = db.Column(db.Boolean, default=False)

    # -------------------CRM LEADS --------------------------------

    can_view_lead = db.Column(db.Boolean, default=False)
    can_add_lead = db.Column(db.Boolean, default=False)
    can_edit_lead = db.Column(db.Boolean, default=False)
    can_delete_lead = db.Column(db.Boolean, default=False)

    # --------------------CRM DEALS -----------------------------------

    can_add_deal = db.Column(db.Boolean, default=False)
    can_view_deal = db.Column(db.Boolean, default=False)
    can_edit_deal = db.Column(db.Boolean, default=False)
    can_delete_deal = db.Column(db.Boolean, default=False)

    # ----------------- CRM ACCOUNTS --------------------------------
    can_add_crm_accounts = db.Column(db.Boolean, default=False)
    can_view_crm_accounts = db.Column(db.Boolean, default=False)
    can_edit_crm_accounts = db.Column(db.Boolean, default=False)
    can_delete_crm_accounts = db.Column(db.Boolean, default=False)

    # ------------------CRM ACTIVITY--------------------------------

    can_create_crm_activity = db.Column(db.Boolean, default=False)
    can_view_crm_activity = db.Column(db.Boolean, default=False)
    can_edit_crm_activity = db.Column(db.Boolean, default=False)
    can_delete_crm_activity = db.Column(db.Boolean, default=False)

    # ------------------CRM CONTANCTS ------------------------------

    can_add_crm_contact = db.Column(db.Boolean, default=False)
    can_view_crm_contact = db.Column(db.Boolean, default=False)
    can_edit_crm_contact = db.Column(db.Boolean, default=False)
    can_delete_crm_contact = db.Column(db.Boolean, default=False)

    # -------------------CRM SETTINGS------------------------------
    can_add_crm_settings = db.Column(db.Boolean, default=False)
    can_view_crm_settings = db.Column(db.Boolean, default=False)
    can_edit_crm_settings = db.Column(db.Boolean, default=False)
    can_delete_crm_settings = db.Column(db.Boolean, default=False)

    # --------------------STOCK ---------------------------------
    can_add_stock = db.Column(db.Boolean, default=False)
    can_view_stock = db.Column(db.Boolean, default=False)
    can_edit_stock = db.Column(db.Boolean, default=False)
    can_delete_stock = db.Column(db.Boolean, default=False)

    # -----------------PURCHASE ------------------------------

    can_add_supplier = db.Column(db.Boolean, default=False)
    can_view_supplier = db.Column(db.Boolean, default=False)
    can_edit_supplier = db.Column(db.Boolean, default=False)
    can_delete_supplier = db.Column(db.Boolean, default=False)

    # ------------------FORMS --------------------------------

    cash_deposit_form_create = db.Column(db.Boolean, default=False)
    cash_deposit_form_view = db.Column(db.Boolean, default=False)
    cash_deposit_form_edit = db.Column(db.Boolean, default=False)
    cash_deposit_form_delete = db.Column(db.Boolean, default=False)

    cash_register_form_create = db.Column(db.Boolean, default=False)
    cash_register_form_view = db.Column(db.Boolean, default=False)
    cash_register_form_edit = db.Column(db.Boolean, default=False)
    cash_register_form_delete = db.Column(db.Boolean, default=False)

    cash_requisition_form_create = db.Column(db.Boolean, default=False)
    cash_requisition_form_view = db.Column(db.Boolean, default=False)
    cash_requisition_form_edit = db.Column(db.Boolean, default=False)
    cash_requisition_form_delete = db.Column(db.Boolean, default=False)

    cash_retirement_form_create = db.Column(db.Boolean, default=False)
    cash_retirement_form_view = db.Column(db.Boolean, default=False)
    cash_retirement_form_edit = db.Column(db.Boolean, default=False)
    cash_retirement_form_delete = db.Column(db.Boolean, default=False)

    claim_form_create = db.Column(db.Boolean, default=False)
    claim_form_view = db.Column(db.Boolean, default=False)
    claim_form_edit = db.Column(db.Boolean, default=False)
    claim_form_delete = db.Column(db.Boolean, default=False)

    material_purchase_form_create = db.Column(db.Boolean, default=False)
    material_purchase_form_view = db.Column(db.Boolean, default=False)
    material_purchase_form_edit = db.Column(db.Boolean, default=False)
    material_purchase_form_delete = db.Column(db.Boolean, default=False)

    material_requisition_form_create = db.Column(db.Boolean, default=False)
    material_requisition_form_view = db.Column(db.Boolean, default=False)
    material_requisition_form_edit = db.Column(db.Boolean, default=False)
    material_requisition_form_delete = db.Column(db.Boolean, default=False)

    payment_voucher_form_create = db.Column(db.Boolean, default=False)
    payment_voucher_form_view = db.Column(db.Boolean, default=False)
    payment_voucher_form_edit = db.Column(db.Boolean, default=False)
    payment_voucher_form_delete = db.Column(db.Boolean, default=False)

    petty_cash_reconciliation_form_create = db.Column(db.Boolean, default=False)
    petty_cash_reconciliation_form_view = db.Column(db.Boolean, default=False)
    petty_cash_reconciliation_form_edit = db.Column(db.Boolean, default=False)
    petty_cash_reconciliation_form_delete = db.Column(db.Boolean, default=False)

    petty_cash_voucher_form_create = db.Column(db.Boolean, default=False)
    petty_cash_voucher_form_view = db.Column(db.Boolean, default=False)
    petty_cash_voucher_form_edit = db.Column(db.Boolean, default=False)
    petty_cash_voucher_form_delete = db.Column(db.Boolean, default=False)

    refund_note_form_create = db.Column(db.Boolean, default=False)
    refund_note_form_view = db.Column(db.Boolean, default=False)
    refund_note_form_edit = db.Column(db.Boolean, default=False)
    refund_note_form_delete = db.Column(db.Boolean, default=False)

    sales_commission_form_create = db.Column(db.Boolean, default=False)
    sales_commission_form_view = db.Column(db.Boolean, default=False)
    sales_commission_form_edit = db.Column(db.Boolean, default=False)
    sales_commission_form_delete = db.Column(db.Boolean, default=False)

    quotation_form_create = db.Column(db.Boolean, default=False)
    quotation_form_view = db.Column(db.Boolean, default=False)
    quotation_form_edit = db.Column(db.Boolean, default=False)
    quotation_form_delete = db.Column(db.Boolean, default=False)

    stock_items_create = db.Column(db.Boolean, default=False)
    stock_items_view = db.Column(db.Boolean, default=False)
    stock_items_edit = db.Column(db.Boolean, default=False)
    stock_items_delete = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs) -> None:
        super(UserRoles, self).__init__(**kwargs)

        if self.role_name == "accountant":
            self.can_view_dashboard = True
            self.can_view_deal = True
            self.can_view_stock = True
            self.can_add_stock = True
            self.can_view_purchase = True
            self.can_add_supplier = True
            self.can_view_forms = True

        elif self.role_name == "operation":
            self.can_view_dashboard = True
            self.can_view_deal = True
            self.can_create_crm_activity = True
            self.can_view_stock = True
            self.can_add_stock = True
            self.can_edit_stock = True
            self.can_view_forms = True

        elif self.role_name == "marketing":
            self.can_view_dashboard = True
            self.can_view_marketing = True
            self.can_do_marketing = True
            self.can_update_marketing = True
            self.can_view_lead = True
            self.can_add_lead = True
            self.can_view_deal = True
            self.can_view_crm_accounts = True
            self.can_view_crm_activity = True
            self.can_create_crm_activity = True
            self.can_view_crm_contacts = True
            self.can_view_forms = True

        elif self.role_name == "sales":
            self.can_view_dashboard = True
            self.can_view_lead = True
            self.can_add_lead = True
            self.can_edit_lead = True
            self.can_convert_lead = True
            self.can_view_deal = True
            self.can_edit_deal = True
            self.can_add_deal = True
            self.can_view_crm_accounts = True
            self.can_view_crm_activity = True
            self.can_create_crm_activity = True
            self.can_view_crm_contacts = True
            self.can_add_contact = True
            self.can_view_crm_settings = True
            self.can_view_stock = True
            self.can_view_forms = True

        elif self.role_name == "administrator":
            self.can_view_dashboard = True
            self.can_edit_dashboard = True
            self.can_delete_dashboard = True
            self.can_view_marketing = True
            self.can_do_marketing = True
            self.can_update_marketing = True
            self.can_delete_marketing = True
            self.can_view_lead = True
            self.can_add_lead = True
            self.can_edit_lead = True
            self.can_convert_lead = True
            self.can_delete_lead = True
            self.can_delete_deal = True
            self.can_view_deal = True
            self.can_edit_deal = True
            self.can_create_deal = True
            self.can_view_crm_accounts = True
            self.can_update_crm_accounts = True
            self.can_delete_crm_accounts = True
            self.can_view_crm_activity = True
            self.can_create_crm_activity = True
            self.can_delete_crm_activity = True
            self.can_add_contact = True
            self.can_view_crm_contacts = True
            self.can_view_crm_settings = True
            self.can_edit_crm_settings = True
            self.can_delete_crm_settings = True
            self.can_view_stock = True
            self.can_add_stock = True
            self.can_edit_stock = True
            self.can_delete_stock = True
            self.can_view_supplier = True
            self.can_add_supplier = True
            self.can_edit_supplier = True
            self.can_delete_supplier = True
            self.can_view_forms = True

        else:
            pass

    def __str__(self) -> str:
        return f"<Role> : {self.role_name}"

    def __repr__(self) -> str:
        return f"<Role> : {self.role_name}"


class Campaign(db.Model):
    __tablename__ = "campaign"
    campaign_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    campaign_owner = db.Column(db.String(120), default="Harlos Containers")
    campaign_name = db.Column(db.String(120), nullable=False)
    campaign_type = db.Column(db.String(120), nullable=True)
    campaign_status = db.Column(db.String(120), nullable=True)
    campaign_message = db.Column(db.String(120), nullable=True)
    contact_type = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(120), nullable=True)
    audience_reached = db.Column(db.Integer, nullable=True)
    expected_revenue = db.Column(db.Float, default=0.0)
    budgeted_cost = db.Column(db.Float, default=0.0)
    actual_cost = db.Column(db.Float, default=0.0)
    expected_response = db.Column(db.String(120), nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    users = db.relationship(Users)

    def __str__(self):
        return f"<id>: {self.campaign_id} <name> :{self.campaign_name}"

    @staticmethod
    def unique_campaigns():
        all_campaigns = Campaign.query.all()
        campaigns = [campaign.campaign_name for campaign in all_campaigns]
        return campaigns

    def __repr__(self):
        return f"<id>: {self.campaign_id} <name> :{self.campaign_name}"


class ContactGroups(db.Model):
    __tablename__ = "contactgroups"

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(120), nullable=True)
    group_count = db.Column(db.Integer, nullable=True)
    group_description = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self):
        return f"<id>: {self.group_id} <name>: {self.group_name}"

    def __repr__(self):
        return f"<id>: {self.group_id} <name>: {self.group_name}"


class CustomerContacts(db.Model):
    __tablename__ = "customercontacts"

    contact_id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(120), nullable=True)
    firstname = db.Column(db.String(120), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    mobile = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(40), nullable=True)
    twitter = db.Column(db.String(100), nullable=True)
    linkedin = db.Column(db.String(100), nullable=True)
    facebook = db.Column(db.String(100), nullable=True)
    skype = db.Column(db.String(100), nullable=True)
    mailing_city = db.Column(db.String(120), nullable=True)
    contact_owner = db.Column(db.String(120), nullable=True)
    added_by = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    group_name = db.Column(db.String(120), default="prospects")
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs) -> None:
        super(CustomerContacts, self).__init__(**kwargs)
        group_exists = ContactGroups.query.filter_by(group_name=self.group_name).first()
        if group_exists:
            group_exists.group_count = group_exists.group_count + 1
            db.session.add(group_exists)
            db.session.commit()
        else:
            new_group = ContactGroups(group_name=self.group_name, group_count=1)
            db.session.add(new_group)
            db.session.commit()

    @property
    def set_contact_name(self):
        return self.contact_name

    @set_contact_name.setter
    def set_contact_name(self, new_contact_name):
        if not isinstance(new_contact_name, str):
            return False
        try:
            self.contact_name = new_contact_name
            self.firstname, *last_name = new_contact_name.split(" ")
            if last_name:
                self.lastname = " ".join(last_name)
        except Exception as bug:
            print(bug)
            return False

    @property
    def new_group_name(self):
        return self.group_name

    @new_group_name.setter
    def new_group_name(self, new_group):
        old_contact_group = ContactGroups.query.filter_by(
            group_name=self.group_name
        ).first()
        if new_group == self.group_name:
            pass
            print("group is the same")
        else:
            if old_contact_group is not None:
                old_contact_group.group_count = old_contact_group.group_count - 1

            group_exist = ContactGroups.query.filter_by(group_name=new_group).first()
            if group_exist:
                group_exist.group_count = group_exist.group_count + 1
                db.session.add(group_exist)
                if old_contact_group is not None:
                    if old_contact_group.group_count == 0:
                        db.session.delete(old_contact_group)
                    else:
                        db.session.add(old_contact_group)
                db.session.commit()
                self.group_name = new_group
                print("group updated")
            else:
                new_contact_group = ContactGroups(group_name=new_group, group_count=1)
                db.session.add(new_contact_group)
                if old_contact_group is not None:
                    if old_contact_group.group_count == 0:
                        db.session.delete(old_contact_group)
                    else:
                        db.session.add(old_contact_group)
                db.session.commit()
                self.group_name = new_group
                print("new group created")

    def __str__(self):
        return f"<name> : {self.firstname}"

    def __repr__(self):
        return f"<name> : {self.firstname}"


class Leads(db.Model):
    __tablename__ = "leads"

    lead_id = db.Column(db.Integer, primary_key=True)
    lead_name = db.Column(db.String(120), nullable=True)
    firstname = db.Column(db.String(120), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    industry = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    group = db.Column(db.String(120), nullable=True)
    lead_source = db.Column(db.String(120), nullable=True)
    lead_owner = db.Column(db.String(120), nullable=True)
    lead_status = db.Column(db.String(120), nullable=True)
    persona = db.Column(db.String(120), nullable=True)
    lead_title = db.Column(db.String(120), nullable=True)
    lead_product = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs):
        super(Leads, self).__init__(**kwargs)
        self.lead_name = f"{self.firstname} {self.lastname}"

    @property
    def full_name(self):
        return self.lead_name

    @full_name.setter
    def full_name(self, new_full_name):
        if not isinstance(new_full_name, str):
            return False
        try:
            self.first_name, *self.last_name = new_full_name.split(" ")
            self.last_name = "".join(str(self.lastname))
        except Exception as bug:
            print(bug)
            return False

    def update_lead_name(self):
        self.lead_name = f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<Lead> {self.lead_name}"

    def __str__(self):
        return f"<Lead> {self.lead_name}"


class InvoiceCounter(db.Model):
    __tablename__ = "invoice_counter"

    invoice_id = db.Column(db.Integer, primary_key=True)
    latest_invoice_number = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return f"InvoiceCounter <{self.invoice_id}> : <{self.latest_invoice_number}>"

    def __str__(self):
        return f"InvoiceCounter <{self.invoice_id}> : <{self.latest_invoice_number}>"


class Deals(db.Model):
    __tablename__ = "deals"

    # ==============Columns adopted from leads ============
    deal_id = db.Column(db.Integer, primary_key=True)
    deal_name = db.Column(db.String(120), nullable=False)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), default="Tanzania")
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    persona = db.Column(db.String(100), nullable=True)
    deal_owner = db.Column(db.String(100), nullable=True)
    dont_edit = db.Column(db.Boolean, default=False)

    # ============= Custom Deal Columns ==================
    account_name = db.Column(db.String(120), nullable=True)
    contact_role = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, default=0.0)
    containers = db.Column(db.String(500), nullable=False)
    no_container_types = db.Column(db.Integer, nullable=False)
    probability = db.Column(db.Float, nullable=True)
    expected_revenue = db.Column(db.Float, nullable=True)
    deal_stage = db.Column(db.String(120), nullable=False)
    invoice_number = db.Column(db.String(120), nullable=True)

    # -------------Invoice detail --------------------------------

    approved_invoice = db.Column(db.Boolean, default=False)
    approved_by = db.Column(db.String(120), nullable=True)
    attached_invoice = db.Column(db.String(120), nullable=True)
    attached_slip = db.Column(db.String(200), nullable=True)
    attached_to_container = db.Column(db.Boolean, default=False)

    # ---------------Deal date data---------------------------------
    created_date = db.Column(db.Date, default=datetime.date.today())
    closing_date = db.Column(db.Date, default=datetime.date.today())
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs):
        super(Deals, self).__init__(**kwargs)
        self.update_expected_revenue()

    def update_expected_revenue(self):
        stage_probability = {
            "Closed Lost to Competition": 0,
            "Closed Lost": 0,
            "Qualification": 0.1,
            "Needs Analysis": 0.2,
            "Value Proposition": 0.4,
            "Identify Decision Makers": 0.6,
            "Proposal/Price Quote": 0.7,
            "Negotiation/Review": 0.9,
            "Closed Won": 1,
        }
        print("getting something")
        print(stage_probability[f"{self.deal_stage}"])
        anything = stage_probability[self.deal_stage]
        # print(anything)
        print("Found anything")
        self.probability = anything
        print(self.amount)
        self.expected_revenue = round(float(self.probability) * float(self.amount))

        if str(self.deal_stage) == "Closed Won":
            target_account = Accounts.query.filter_by(
                account_name=self.account_name
            ).first()
            target_account.account_type = "customer"
            db.session.add(target_account)
            db.session.commit()
            print(f"<{target_account} is now a customer")

    def __repr__(self):
        return f"<Deal> {self.deal_name}"

    def __str__(self):
        return f"<Deal> {self.deal_name}"


class Accounts(db.Model):
    __tablename__ = "accounts"

    # ================Custom Account Column===============
    account_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(120), nullable=False)
    account_type = db.Column(db.String(50), default="prospect")
    account_owner = db.Column(db.String(100), nullable=True)
    # ========General info adopted from Deal ===========
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    firstname = db.Column(db.String(120), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    group = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    persona = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    source = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs):
        super(Accounts, self).__init__(**kwargs)
        if self.company:
            self.account_name = self.company
        else:
            self.account_name = f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<Account Name> {self.account_name}"

    def __str__(self):
        return f"<Account Name> {self.account_name}"


class CrmContacts(db.Model):
    __tablename__ = "crm_contacts"

    contact_id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(120), nullable=False)
    contact_owner = db.Column(db.String(100), nullable=True)

    # ========General info adopted from Deal ===========
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    contact_name = db.Column(db.String(120), nullable=True)
    firstname = db.Column(db.String(120), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    company = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    persona = db.Column(db.String(100), nullable=True)
    contact_role = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __init__(self, **kwargs):
        super(CrmContacts, self).__init__(**kwargs)
        self.contact_name = f"{self.firstname} {self.lastname}"

    def __repr__(self):
        return f"<Contact> {self.contact_name}"

    def __str__(self):
        return f"<Contact> {self.contact_name}"


class CRM_Setting(db.Model):
    __tablename__ = "crm_setting"
    setting_id = db.Column(db.Integer, primary_key=True)
    lead_sources = db.Column(db.String(300), nullable=True)
    lead_status = db.Column(db.String(300), nullable=True)
    lead_industries = db.Column(db.String(300), nullable=True)
    lead_stages = db.Column(db.String(300), nullable=True)
    deal_types = db.Column(db.String(300), nullable=True)
    lead_persona = db.Column(db.String(300), nullable=True)
    contact_roles = db.Column(db.String(300), nullable=True)
    activity_types = db.Column(db.String(300), nullable=True)

    def __repr__(self) -> str:
        return f"<Setting ID> {self.setting_id}"

    def __str__(self) -> str:
        return f"<Setting ID> {self.setting_id}"


class Activities(db.Model):
    __tablename__ = "activities"

    a_id = db.Column(db.Integer, primary_key=True)
    a_name = db.Column(db.String(120), nullable=True)
    a_type = db.Column(db.String(120), nullable=True)
    a_status = db.Column(db.String(50), nullable=True)
    a_description = db.Column(db.String(120), nullable=True)
    a_account = db.Column(db.String(120), nullable=False)
    a_owner = db.Column(db.String(120), nullable=False)
    a_time = db.Column(db.Date, default=datetime.date.today())
    activity_owner = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return f"<Activity Name> {self.activitiy_name}"

    def __str__(self):
        return f"<Activity Name> {self.activitiy_name}"


class Stock(db.Model):
    __tablename__ = "stock"

    stock_id = db.Column(db.Integer, primary_key=True)
    container_number = db.Column(db.String(120), nullable=False)
    unit = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    in_quantity = db.Column(db.Integer, nullable=False)
    out_quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return f"<Stock {self.stock_id}> : Container <{self.container_number}>"

    def __str__(self):
        return f"<Stock {self.stock_id}> : Container <{self.container_number}>"


class Container(db.Model):
    __tablename__ = "container"

    container_id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default="Available")
    on_hold_reason = db.Column(db.Text, nullable=True)
    size = db.Column(db.String(20), nullable=True)
    condition = db.Column(db.String(120), nullable=True)
    category = db.Column(db.String(120), nullable=True)
    supplier = db.Column(db.String(120), nullable=True)
    purchase_price = db.Column(db.Float, nullable=True)
    sale_price = db.Column(db.Float, nullable=True)
    tax = db.Column(db.Integer, nullable=True)
    depot = db.Column(db.String(120), nullable=True)
    main_image = db.Column(db.String(200), nullable=True)
    visibility_on_website = db.Column(db.Boolean, default=False)
    general_condition = db.Column(db.String(200), nullable=True)

    invoice_number = db.Column(db.String(120), nullable=True)
    outward_no = db.Column(db.String(120), nullable=True)
    truck_no = db.Column(db.String(120), nullable=True)
    driver_name = db.Column(db.String(120), nullable=True)
    driver_license = db.Column(db.String(120), nullable=True)
    order_invoice = db.Column(db.String(200), nullable=True)

    payment_confirmed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date, default=datetime.date.today())
    stock_in_date = db.Column(db.Date, default=datetime.date.today())
    release_date = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def update_release_date(self):
        self.release_date = datetime.datetime.utcnow()

    @property
    def depot_days(self):
        return (self.release_date.date() - self.stock_in_date).days

    def __repr__(self):
        return f"<Container {self.container_id}> : {self.number}"

    def __str__(self):
        return f"<Container {self.container_id}> : {self.number}"


class Suppliers(db.Model):
    __tablename__ = "suppliers"
    supplier_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    prev_credit_balance = db.Column(db.Float, nullable=True)
    product_or_service = db.Column(db.String(100), nullable=True)
    payment_details = db.Column(db.String(120), nullable=True)
    supplier_type = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return f"<Supplier {self.supplier_id}> : {self.name}"

    def __str__(self):
        return f"<Supplier {self.supplier_id}> : {self.name}"


class Orders(db.Model):
    __tablename__ = "orders"
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"))
    order_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, nullable=False)
    invoice_number = db.Column(db.String(50), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    users = db.relationship(Users)
    accounts = db.relationship(Accounts)
    date_created = db.Column(db.Date, default=datetime.date.today())

    def __repr__(self):
        return f"<Orders {self.user_id}> : {self.invoice_number}"

    def __str__(self):
        return f"<Orders {self.user_id}> : {self.invoice_number}"


class Forms(db.Model):
    __tablename__ = "forms"

    form_id = db.Column(db.Integer, primary_key=True)
    form_type = db.Column(db.String(120), nullable=False)
    reference = db.Column(db.String(120), nullable=True)
    currency = db.Column(db.String(120), default="TZS")
    status = db.Column(db.String(120), default="Pending")
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __str__(self) -> str:
        return f"<Form {self.form_id}> : {self.form_type}"

    def __repr__(self) -> str:
        return f"<Form {self.form_id}> : {self.form_type}"


class CashDepositForm(db.Model):
    __tablename__ = "cashdepositform"

    form_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), default="Pending")
    account_no = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    amount_in_words = db.Column(db.String(120), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    reference = db.Column(db.String(120), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<CashDepositForm {self.form_id}>"

    def __repr__(self):
        return f"<CashDepositForm {self.form_id}>"


class CashRegisterForm(db.Model):
    __tablename__ = "cashregisterform"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    paid_to = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    amount_in_words = db.Column(db.String(120), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    requested_by = db.Column(db.String(120), nullable=True)
    requested_to = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<CashRegisterForm {self.form_id}>"

    def __repr__(self):
        return f"<CashRegisterForm {self.form_id}>"


class CashRequisitionForm(db.Model):
    __tablename__ = "cashrequisitionform"

    form_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), default="Pending")
    account_no = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    description_of_expense = db.Column(db.String(120), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    authorized_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    reference = db.Column(db.String(120), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<CashRequisitionForm {self.form_id}>"

    def __repr__(self):
        return f"<CashRequisitionForm {self.form_id}>"


class CashRetirementForm(db.Model):
    __tablename__ = "cashretirementform"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    start_balance = db.Column(db.Float, nullable=True)
    end_balance = db.Column(db.Float, nullable=True)
    start_date = db.Column(db.Date, default=datetime.date.today())
    end_date = db.Column(db.Date, default=datetime.date.today())
    expenditure = db.Column(db.String(500), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    cash_issued_by = db.Column(db.String(120), nullable=True)
    cash_received_by = db.Column(db.String(120), nullable=True)
    balance_returned_by = db.Column(db.String(120), nullable=True)
    balance_received_by = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<CashRetirementForm {self.form_id}>"

    def __repr__(self):
        return f"<CashRetirementForm {self.form_id}>"


class ClaimForm(db.Model):
    __tablename__ = "claimform"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    employee_name = db.Column(db.String(120), nullable=True)
    employee_id = db.Column(db.String(120), nullable=True)
    manager_name = db.Column(db.String(120), nullable=True)
    department = db.Column(db.String(120), nullable=True)
    bussiness_purpose = db.Column(db.String(300), nullable=True)
    claim_expenditure = db.Column(db.Text, nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    expense_start_date = db.Column(db.Date, default=datetime.date.today())
    expense_end_date = db.Column(db.Date, default=datetime.date.today())
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<ClaimForm {self.form_id}> {self.employee_name}"

    def __repr__(self):
        return f"<ClaimForm {self.form_id}> {self.employee_name}"


class StockItems(db.Model):
    __tablename__ = "stockitems"
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), nullable=True)
    item_price = db.Column(db.Float, nullable=True)
    item_description = db.Column(db.String(120), nullable=True)
    stock_amount = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def add_items(self, quantity):
        quantity = abs(quantity)
        self.stock_amount = self.stock_amount + quantity

    def use_items(self, quantity):
        quantity = abs(quantity)
        is_too_much = self.stock_amount - quantity
        if is_too_much < 0.0:
            print("That amount is too much than what present")
            return False
        self.stock_amount = is_too_much

    def __repr__(self) -> str:
        return f"<StockItems {self.item_id}> : <{self.item_name}>"

    def __repr__(self) -> str:
        return f"<StockItems {self.item_id}> : <{self.item_name}>"


class MaterialPurchaseForm(db.Model):
    __tablename__ = "materialpurchaseform"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    total_amount = db.Column(db.Float, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    purchases = db.Column(db.String(500), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    requested_by = db.Column(db.String(120), nullable=True)
    requested_to = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    @property
    def _status(self):
        return self.status

    @_status.setter
    def _status(self, new_status):
        new_status = new_status.strip()
        what = new_status == "Approved"
        print(f"new status is {new_status} {what}")
        if new_status == "Approved":
            items = json.loads(self.purchases)
            for item in items:
                item_exist = StockItems.query.filter_by(
                    item_name=item["item_name"]
                ).first()
                if not item_exist:
                    new_stock_item = StockItems(
                        item_name=item.get("item_name"),
                        item_price=item.get("amount"),
                        stock_amount=item.get("quantity"),
                        item_description=item.get("description"),
                    )
                    db.session.add(new_stock_item)
                else:
                    item_exist.add_stock(item.get("quantity"))
                    db.session.add(item_exist)
            db.session.commit()
            self.status = new_status
            print("Stock Items updated successfully")
        else:
            self.status = new_status
            db.session.commit()
            print("Stock Items skipped")

    def __str__(self):
        return f"<MaterialPurchaseForm {self.form_id}>"

    def __repr__(self):
        return f"<MaterialPurchaseForm {self.form_id}>"


class MaterialRequisitionForm(db.Model):
    __tablename__ = "materialrequisitionform"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    requisitions = db.Column(db.Text, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    requested_by = db.Column(db.String(120), nullable=True)
    requested_to = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<MaterialRequisitionForm {self.form_id}>"

    def __repr__(self):
        return f"<MaterialPurchaseForm {self.form_id}>"


class PaymentVoucher(db.Model):
    __tablename__ = "paymentvoucher"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    pay_to = db.Column(db.String(120), nullable=True)
    payto_no = db.Column(db.String(50), nullable=True)
    voucher_type = db.Column(db.String(50), nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    voucher_items = db.Column(db.Text, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<PaymentVoucher {self.form_id}>"

    def __repr__(self):
        return f"<PaymentVoucher {self.form_id}>"


class PettyCashReconciliation(db.Model):
    __tablename__ = "pettycashreconciliation"

    form_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(30), default="Pending")
    attachment = db.Column(db.String(200), nullable=True)
    reference = db.Column(db.String(120), nullable=True)
    cheq_no = db.Column(db.String(120), nullable=True)
    orm_no = db.Column(db.String(120), nullable=True)

    # --------------Petty Cash vouchers -----------------

    start_p_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_p_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # -------------crm summary --------------------------
    prev_date = db.Column(db.Date, default=datetime.date.today())
    withdraw_date = db.Column(db.Date, default=datetime.date.today())
    balance_bd = db.Column(db.Float, nullable=True)
    additional_cash = db.Column(db.Float, nullable=True)
    cash_from = db.Column(db.String(120), nullable=True)
    total_amount = db.Column(db.Float, nullable=True)

    rec_items = db.Column(db.Text, nullable=True)

    cash_handler = db.Column(db.String(120), nullable=True)
    finance_handler = db.Column(db.String(120), nullable=True)
    ceo_handler = db.Column(db.String(120))
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)

    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<PettyCashRenconciliation {self.form_id}>"

    def __repr__(self):
        return f"<PettyCashRenconciliation {self.form_id}>"


class PettyCashVoucher(db.Model):
    __tablename__ = "pettycashvoucher"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    payment_made_to = db.Column(db.String(120), nullable=True)
    voucher_no = db.Column(db.String(120), nullable=True)
    voucher_items = db.Column(db.Text, nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(300), nullable=True)
    requisition_ref = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    @property
    def requisition(self):
        return self.requisition_ref

    @requisition.setter
    def requisition(self, ref):
        target_ref = CashRequisitionForm.query.filter_by(reference=ref).first()
        if target_ref:
            self.total_amount = target_ref.amount
            self.description = target_ref.description_of_expense
        self.requisition_ref = ref

    @staticmethod
    def get_rencoliation(start_date, end_date):
        all_vouchers = PettyCashVoucher.query.all()
        target_vouchers = []
        for voucher in all_vouchers:
            d = voucher.date_created
            date_created = datetime.datetime(d.year, d.month, d.day)
            if end_date > date_created > start_date:
                target_vouchers.append(voucher)
                continue
        return target_vouchers


class RefundNote(db.Model):
    __tablename__ = "refundnote"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    name = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    add_info = db.Column(db.String(200), nullable=True)
    original_price = db.Column(db.Float, nullable=True)
    adjusted_price = db.Column(db.Float, nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    proforma_invoice_no = db.Column(db.String(120), nullable=True)
    proforma_invoice_amount = db.Column(db.Float, nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<RefundNote {self.form_id}>"

    def __repr__(self):
        return f"<RefundNote {self.form_id}>"


class SalesCommission(db.Model):
    __tablename__ = "salecommission"

    form_id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    name = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    commissions = db.Column(db.Text, nullable=True)
    total_amount = db.Column(db.Float, nullable=True)
    attachment = db.Column(db.String(200), nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    approved_by = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self):
        return f"<SalesCommission {self.form_id}>"

    def __repr__(self):
        return f"<SalesCommission {self.form_id}>"


class QuatationForm(db.Model):
    __tablename__ = "quotationform"

    form_id = db.Column(db.Integer, primary_key=True)
    attachment = db.Column(db.String(200), nullable=True)
    reference = db.Column(db.String(120), nullable=True)
    status = db.Column(db.String(30), default="Pending")
    name = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(120), nullable=True)
    quotation_date = db.Column(db.Date, default=datetime.date.today())
    expiry_date = db.Column(db.Date, default=datetime.date.today())
    quotation_no = db.Column(db.String(120), nullable=True)
    sales_person = db.Column(db.String(120), nullable=True)
    amount = db.Column(db.Float, nullable=True)
    tax_collected = db.Column(db.Float, nullable=True)
    prepared_by = db.Column(db.String(120), nullable=True)
    date_created = db.Column(db.Date, default=datetime.date.today())
    updated_on = db.Column(db.Date, default=datetime.date.today())

    def __str__(self) -> str:
        return f"<Quotation {self.form_id}> {self.name}"

    def __repr__(self) -> str:
        return f"<Quotation {self.form_id}> {self.name}"


class GeneralSetting(db.Model):
    __tablename__ = "generalsetting"

    setting_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    logo = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120))
    telephone = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    tax = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(20), nullable=True)

    def __repr__(self) -> str:
        return f"<GeneralSetting {self.setting_id}"

    def __str__(self) -> str:
        return f"<GeneralSetting {self.setting_id}"


class customerStatistics(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    customers = db.Column(db.String(120), nullable=False)
    countries = db.Column(db.String(120), nullable=False)
    ports = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"<customerStatistics {self.id}>"

    def __str__(self) -> str:
        return f"<customerStatistics {self.id}>"


class Testimonials(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    review = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Testimonial {self.id}> : {self.title}"

    def __str__(self):
        return f"<Testimonial {self.id}> : {self.title}"


class ItemsToDelete(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(120), nullable=False)
    reason = db.Column(db.String(120), nullable=True)
    requested_by = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"<{self.table_name}> : {self.item_id}"
