import os
import json
import time
import datetime
from typing import Any, List
import flask_login
from flask import current_app as app
from flask_login import login_required
from erp.crm.crm import format_the_date
from erp.stock.stock import format_the_price
from erp.purchase.purchase import load_all_suppliers
from erp.general import *
from flask import Blueprint, url_for, redirect, render_template, request


forms_bp = Blueprint(
    "forms_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static",
    static_url_path="assets",
)


def generate_reference_number(form_type: str) -> str:
    try:
        form_abbrev = extensions.get(form_type)
        timestamp = str(round(time.time()))
        reference = f"HCL/FN/{form_abbrev}/{timestamp}"
        return reference
    except Exception as bug:
        print("Failed to generate reference number")
        print(bug)
        return ""


def save_attachement(form_type: str, reference: str):
    try:
        data = attachment_paths.get(form_type)
        pdf_path = ""
        if data:
            reference = reference.replace("/", "-")
            pdf_path = f"{data}/{reference}.pdf"
            if not os.path.exists("erp/static/img/forms"):
                os.mkdir("erp/static/img/forms")
            if not os.path.exists(data):
                os.mkdir(data)

            pdf_attachment = request.files.get("attachment")
            pdf_attachment.save(pdf_path)
            pdf_path = pdf_path[11:]
        return pdf_path
    except Exception as bug:
        print(f"Failed {form_type} attachment")
        print(bug)
        return ""


def add_cash_deposit_form(cash_deposit_data: dict) -> bool:
    try:
        with app.app_context():
            account_no = cash_deposit_data.get("account_no")
            amount = cash_deposit_data.get("amount")
            amount_in_words = cash_deposit_data.get("amount_in_words")
            requested_by = cash_deposit_data.get("requested_by")
            prepared_by = cash_deposit_data.get("prepared_by")
            approved_by = cash_deposit_data.get("signed_by")
            reference = generate_reference_number("CashDepositForm")
            attachment = save_attachement("CashDepositForm", reference)
            description = cash_deposit_data.get("description_of_expense")
            amount = format_the_amount(amount)
            print(f"{prepared_by} testing damn it")

            new_cash_deposit = CashDepositForm(
                account_no=account_no,
                amount=amount,
                amount_in_words=amount_in_words,
                prepared_by=prepared_by,
                approved_by=approved_by,
                attachment=attachment,
                reference=reference,
                description_of_expense=description
            )

            new_form = Forms(
                form_type="CashDepositForm",
                reference=reference,
            )

            db.session.add(new_cash_deposit)
            db.session.add(new_form)
            db.session.commit()
            print("Cash deposit added ")
            return True
    except Exception as bug:
        print("Failed to add cash deposit form data")
        print(bug)
        return False


def add_cash_register_form(cash_register_data: dict) -> bool:
    try:
        with app.app_context():
            paid_to = cash_register_data.get("paid_to")
            amount = cash_register_data.get("amount")
            amount_in_words = cash_register_data.get("amount_in_words")
            prepared_by = cash_register_data.get("prepared_by")
            requested_by = cash_register_data.get("requested_by")
            requested_to = cash_register_data.get("requested_to")
            reference = generate_reference_number("CashRegisterForm")
            description = cash_register_data.get("description_of_expense")
            attachement = save_attachement("CashRegisterForm", reference)

            amount = format_the_price(amount)
            new_cash_register = CashRegisterForm(
                reference=reference,
                paid_to=paid_to,
                amount=amount,
                attachment=attachement,
                amount_in_words=amount_in_words,
                prepared_by=prepared_by,
                requested_by=requested_by,
                requested_to=requested_to,
                description_of_expense=description,
            )
            new_form = Forms(form_type="CashRegisterForm", reference=reference)
            db.session.add(new_cash_register)
            db.session.add(new_form)
            db.session.commit()
            print("Cash Register Form added")
            return True
    except Exception as bug:
        print("Failed to cash register form data")
        print(bug)
        return False


def get_current_account_admin():
    with app.app_context():
        admin = Users.query.filter_by(role="administrator").first()
        if admin:
            return admin.fullname
        return "Empty Role (absent)"


def get_currrent_accountant():
    with app.app_context():
        accountant = Users.query.filter_by(role="accountant").first()
        if accountant:
            return accountant.fullname
        return "Empty Role (absent)"


def add_cash_requisition_form(cash_requisition_data: dict) -> bool:
    try:
        with app.app_context():
            amount = cash_requisition_data.get("amount")
            department = cash_requisition_data.get("department")
            description_of_expense = cash_requisition_data.get("description_of_expense")
            requested_by = cash_requisition_data.get("requested_by")
            signed_by = cash_requisition_data.get("signed_by")
            authorized_by = cash_requisition_data.get("authorized_by")
            date_submiited = cash_requisition_data.get("date_submitted")
            date_submiited = format_the_date(date_submiited)
            reference = generate_reference_number("CashRequisitionForm")
            attachment = save_attachement("CashRequisitionForm", reference)

            new_cash_requisition = CashRequisitionForm(
                reference=reference,
                amount=amount,
                department=department,
                prepared_by=requested_by,
                authorized_by=authorized_by,
                approved_by=signed_by,
                date_created=date_submiited,
                attachment=attachment,
                description_of_expense=description_of_expense,
            )
            new_form = Forms(form_type="CashRequisitionForm", reference=reference)
            db.session.add(new_cash_requisition)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to cash requisition form data")
        print(bug)
        return False


def get_no_expenditure(form_data: Any) -> int:
    try:
        index = 0
        while form_data.get(f"no_of_expenditure_new{index}"):
            index = index + 1
        print(index)
        return index
    except Exception as bug:
        print("Failed to get no of expenditure")
        print(bug)
        return 0


def add_cash_retirement_form(cash_retirement_data: dict) -> bool:
    try:
        with app.app_context():
            start_balance = cash_retirement_data.get("start_balance")
            start_date = cash_retirement_data.get("start_date")
            end_balance = cash_retirement_data.get("end_balance")
            end_date = cash_retirement_data.get("end_date")
            cash_issued_by = cash_retirement_data.get("cash_issued_by")
            cash_received_by = cash_retirement_data.get("cash_received_by")
            balance_returned_by = cash_retirement_data.get("balance_returned_by")
            balance_received_by = cash_retirement_data.get("balance_received_by")
            description_of_expense = cash_retirement_data.get("description_of_expense")
            reference = generate_reference_number("CashRetirementForm")
            attachment = save_attachement("CashRetirementForm", reference)

            start_balance = format_the_price(start_balance)
            end_balance = format_the_price(end_balance)
            start_date = format_the_date(start_date)
            end_date = format_the_date(end_date)
            no_of_expenditure = get_no_expenditure(cash_retirement_data)
            expenditure = create_retirement_expenditure(
                cash_retirement_data, no_of_expenditure
            )
            new_cash_retirement = CashRetirementForm(
                reference=reference,
                start_balance=start_balance,
                start_date=start_date,
                end_balance=end_balance,
                end_date=end_date,
                expenditure=expenditure,
                attachment=attachment,
                cash_issued_by=cash_issued_by,
                cash_received_by=cash_received_by,
                balance_returned_by=balance_returned_by,
                balance_received_by=balance_received_by,
                description_of_expense= description_of_expense
            )
            new_form = Forms(form_type="CashRetirementForm", reference=reference)
            db.session.add(new_cash_retirement)
            db.session.add(new_form)
            db.session.commit()
            print("Retirement data added successfully")
    except Exception as bug:
        print("Failed to cash retirement form data")
        print(bug)
        return False


def create_retirement_expenditure(retirement_data: dict, no: int) -> dict:
    try:
        total_expenditure = []
        for index in range(no):
            e_date = retirement_data.get(f"e_date_new{index}")
            e_expense = retirement_data.get(f"e_expense_new{index}")
            e_amount = retirement_data.get(f"e_amount_new{index}")
            expenditure = {
                "date": e_date,
                "expense": e_expense,
                "amount": e_amount,
            }
            total_expenditure.append(expenditure)
        return json.dumps(total_expenditure)
    except Exception as bug:
        print("Failed to create expenditure data")
        print(bug)
        return False


def get_no_claim_expenditure(claim_data: dict) -> int:
    try:
        index = 0
        while claim_data.get(f"no_of_claim_expenditure_new{index}"):
            index = index + 1
        return index
    except Exception as bug:
        print("Failed to get claim expenditure")
        print(bug)
        return 0


def get_claim_expenditure(claim_data: dict, no: int) -> str:
    try:
        expenditures = []
        for index in range(no):
            expenditure = {
                "date": claim_data.get(f"date_claimed_{index}"),
                "description": claim_data.get(f"description_new{index}"),
                "category": claim_data.get(f"category_new{index}"),
                "cost": claim_data.get(f"cost_new{index}"),
            }
            expenditures.append(expenditure)
        return json.dumps(expenditures)
    except Exception as bug:
        print("Failed to generated claim expenditure data")
        print(bug)
        return ""


def add_claim_form(claim_data: dict) -> bool:
    try:
        with app.app_context():
            employee_name = claim_data.get("employee_name")
            employee_id = claim_data.get("employee_id")
            manager_name = claim_data.get("manager_name")
            department = claim_data.get("department")
            expense_start_date = claim_data.get("expense_start_date")
            expense_end_date = claim_data.get("expense_end_date")
            bussiness_purpose = claim_data.get("bussiness_purpose")
            reference = generate_reference_number("ClaimForm")
            attachment = save_attachement("ClaimForm", reference)
            description = claim_data.get("description_of_expense")

            expense_start_date = format_the_date(expense_start_date)
            expense_end_date = format_the_date(expense_end_date)
            no_expenditures = get_no_claim_expenditure(claim_data)
            claim_expenditures = get_claim_expenditure(claim_data, no_expenditures)
            new_claim = ClaimForm(
                reference=reference,
                employee_name=employee_name,
                employee_id=employee_id,
                manager_name=manager_name,
                department=department,
                attachment=attachment,
                bussiness_purpose=bussiness_purpose,
                expense_start_date=expense_start_date,
                expense_end_date=expense_end_date,
                claim_expenditure=claim_expenditures,
                description_of_expense = description
            )
            new_form = Forms(form_type="ClaimForm", reference=reference)
            db.session.add(new_claim)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to claim form data")
        print(bug)
        return False


def get_no_purchases(material_purchases: dict) -> int:
    try:
        index = 0
        while material_purchases.get(f"no_of_purchases_new{index}"):
            index = index + 1
        return index
    except Exception as bug:
        print("Failed to get no of purchases")
        print(bug)
        return 0


def get_purchase_details(purchases_data: dict, no: int) -> tuple:
    try:
        purchases = []
        total_amount = 0
        for index in range(no):
            amount = purchases_data.get(f"amount_new{index}")
            quantity = purchases_data.get(f"quantity_new{index}")
            amount = format_the_price(amount)
            quantity = format_the_price(quantity)
            purchase = {
                "item_name": purchases_data.get(f"item_name_new{index}"),
                "description": purchases_data.get(f"description_new{index}"),
                "quantity": quantity,
                "amount": amount,
                "total_amount": quantity * amount,
            }
            purchases.append(purchase)
            total_amount = total_amount + (amount * quantity)
        purchases = json.dumps(purchases)
        return [purchases, total_amount]
    except Exception as bug:
        print("Failed to get purchase details")
        print(bug)
        return None


def add_material_purchase_form(material_purchase_data: dict) -> bool:
    try:
        with app.app_context():
            prepared_by = material_purchase_data.get("prepared_by")
            requested_by = material_purchase_data.get("requested_by")
            requested_to = material_purchase_data.get("requested_to")
            description = material_purchase_data.get("description_of_expense")
            reference = generate_reference_number("MaterialPurchaseForm")
            attachement = save_attachement("MaterialPurchaseForm", reference)
            no_of_purchase = get_no_purchases(material_purchase_data)
            total_amount, purchases = 0, []
            if no_of_purchase:
                purchases, total_amount = get_purchase_details(
                    material_purchase_data, no_of_purchase
                )
            new_material_purchase = MaterialPurchaseForm(
                reference=reference,
                total_amount=total_amount,
                purchases=purchases,
                attachment=attachement,
                prepared_by=prepared_by,
                requested_by=requested_by,
                requested_to=requested_to,
                description_of_expense=description
            )
            new_form = Forms(form_type="MaterialPurchaseForm", reference=reference)
            db.session.add(new_material_purchase)
            db.session.add(new_form)
            db.session.commit()
            print("Material purchase case submitted successfully")
    except Exception as bug:
        print("Failed material purchase form data")
        print(bug)
        return False


def get_no_material_requisition(material_req_data: dict) -> int:
    try:
        index = 0
        while material_req_data.get(f"no_material_req_new{index}"):
            index = index + 1
        return index
    except Exception as bug:
        print("Failed to add no of material requisition")
        print(bug)
        return 0


def get_material_requisitions(m_requisitions: dict, no_requisitions: int) -> str:
    try:
        material_requisitions = []
        for index in range(no_requisitions):
            requisition = {
                "item_name": m_requisitions.get(f"item_name_new{index}"),
                "description": m_requisitions.get(f"description_new{index}"),
                "quantity": m_requisitions.get(f"quantity_new{index}"),
                "date_required": m_requisitions.get(f"date_required_new{index}"),
            }
            material_requisitions.append(requisition)
        return json.dumps(material_requisitions)
    except Exception as bug:
        print("Failed to get material requisitions")
        print(bug)
        return ""


def add_material_requisition_form(material_requisition_data: dict) -> bool:
    try:
        with app.app_context():
            prepared_by = material_requisition_data.get("prepared_by")
            requested_by = material_requisition_data.get("requested_by")
            requested_to = material_requisition_data.get("requested_to")
            description = material_requisition_data.get("description_of_expense")
            reference = generate_reference_number("MaterialRequisitionForm")
            attachment = save_attachement("MaterialRequisitionForm", reference)

            no_of_material_req = get_no_material_requisition(material_requisition_data)
            requisitions = get_material_requisitions(
                material_requisition_data, no_of_material_req
            )
            new_material_requisition = MaterialRequisitionForm(
                reference=reference,
                attachment=attachment,
                requisitions=requisitions,
                prepared_by=prepared_by,
                requested_by= requested_by,
                requested_to=requested_to,
                description_of_expense= description,
            )
            new_form = Forms(form_type="MaterialRequisitionForm", reference=reference)
            db.session.add(new_material_requisition)
            db.session.add(new_form)
            db.session.commit()
            print("Material Requistions form")
    except Exception as bug:
        print("Failed material purchase form data")
        print(bug)
        return False


def get_no_payment_vouchers(payment_voucher_data: dict) -> bool:
    try:
        index = 0
        while payment_voucher_data.get(f"no_payment_vouchers_new{index}"):
            index += 1
        return index
    except Exception as bug:
        print("Failed to get no of payment vouchers")
        print(bug)
        return 0


def get_payment_voucher_items(payment_voucher_data: dict, no: int) -> List:
    try:
        payment_voucher_items = []
        total_amount = 0.0
        for index in range(no):
            payment_voucher_data.get(f"amount_new{index}")
            amount = payment_voucher_data.get(f"amount_new{index}")
            amount = format_the_price(amount)
            payment_voucher_item = {
                "particulars": payment_voucher_data.get(f"particulars_new{index}"),
                "reference": payment_voucher_data.get(f"reference_new{index}"),
                "amount": amount,
            }
            payment_voucher_items.append(payment_voucher_item)
            total_amount += amount
        return total_amount, payment_voucher_items
    except Exception as bug:
        print("Failed to get payment voucher items")
        print(bug)
        return 0, []


def add_payment_voucher_form(payment_voucher_data: dict) -> bool:
    try:
        with app.app_context():
            pay_to = payment_voucher_data.get("pay_to")
            payto_no = payment_voucher_data.get("payto_no")
            date_made = payment_voucher_data.get("date_made")
            voucher_type = payment_voucher_data.get("voucher_type")
            reference = generate_reference_number("PaymentVoucher")
            attachement = save_attachement("PaymentVoucher", reference)
            description = payment_voucher_data.get("description_of_expense")

            date_made = format_the_date(date_made)
            no_payment_vouchers = get_no_payment_vouchers(payment_voucher_data)
            total_amount, payment_voucher_items = get_payment_voucher_items(
                payment_voucher_data, no_payment_vouchers
            )

            new_payment_voucher = PaymentVoucher(
                reference=reference,
                pay_to=pay_to,
                payto_no=payto_no,
                attachment=attachement,
                date_created=date_made,
                voucher_type=voucher_type,
                total_amount=total_amount,
                voucher_items=json.dumps(payment_voucher_items),
                description_of_expense=description
            )
            new_form = Forms(form_type="PaymentVoucher", reference=reference)
            db.session.add(new_payment_voucher)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to add payment voucher form data")
        print(bug)
        return False


def get_no_rec_items(pettycash_rec_data: dict) -> int:
    try:
        index = 0
        while pettycash_rec_data.get(f"no_rec_items_new{index}"):
            index += 1
        return index
    except Exception as bug:
        print("Failed to get no of rec items")
        print(bug)
        return 0


def get_rec_items(pettycash_rec_data: dict, no: int) -> List:
    try:
        rec_items = []
        for index in range(no):
            new_rec_item = {
                "sn": index + 1,
                "date": pettycash_rec_data.get(f"date_new{index}"),
                "description": pettycash_rec_data.get(f"description_new{index}"),
                "amount": pettycash_rec_data.get(f"amount_new{index}"),
            }
            rec_items.append(new_rec_item)
        return rec_items
    except Exception as bug:
        print("Failed to get rec items")
        print(bug)
        return []


def add_PettyCashReconciliation(pettycash_rec_data: dict) -> bool:
    try:
        with app.app_context():
            cheq_no = pettycash_rec_data.get("cheq_no")
            orm_no = pettycash_rec_data.get("orm_no")
            prev_date = pettycash_rec_data.get("prev_date")
            withdraw_date = pettycash_rec_data.get("withdraw_date")
            balance_bd = pettycash_rec_data.get("balance_bd")
            additional_cash = pettycash_rec_data.get("additional_cash")
            cash_from = pettycash_rec_data.get("cash_from")
            total_amount = pettycash_rec_data.get("total_amount")
            cash_handler = pettycash_rec_data.get("cash_handler")
            finance_handler = pettycash_rec_data.get("finance_handler")
            ceo_handler = pettycash_rec_data.get("ceo_handler")
            start_p_date = pettycash_rec_data.get("start_p_date")
            end_p_date = pettycash_rec_data.get("end_p_date")
            reference = generate_reference_number("PettyCashReconciliationForm")
            attachment = save_attachement("PettyCashReconciliation", reference)
            description = pettycash_rec_data.get("description_of_expense")

            prev_date = format_the_date(prev_date)
            start_p_date = format_the_date(start_p_date)
            end_p_date = format_the_date(end_p_date)
            withdraw_date = format_the_date(withdraw_date)
            balance_bd = format_the_price(balance_bd)
            additional_cash = format_the_price(additional_cash)
            total_amount = format_the_price(total_amount)

            no_items = get_no_rec_items(pettycash_rec_data)
            rec_items = get_rec_items(pettycash_rec_data, no_items)

            new_petty_cash_reconciliation = PettyCashReconciliation(
                reference=reference,
                cheq_no=cheq_no,
                orm_no=orm_no,
                rec_items=json.dumps(rec_items),
                prev_date=prev_date,
                withdraw_date=withdraw_date,
                balance_bd=balance_bd,
                additional_cash=additional_cash,
                cash_from=cash_from,
                attachment=attachment,
                total_amount=total_amount,
                start_p_date=start_p_date,
                end_p_date=end_p_date,
                cash_handler=cash_handler,
                finance_handler=finance_handler,
                ceo_handler=ceo_handler,
                description_of_expense=description
            )
            new_form = Forms(form_type="PettyCashReconciliation", reference=reference)
            db.session.add(new_petty_cash_reconciliation)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to add petty cash reconciliation data")
        print(bug)
        return False


def get_no_petty_cash_voucher(petty_voucher_data: dict) -> int:
    try:
        index = 0
        while petty_voucher_data.get(f"no_pc_voucher_new{index}"):
            index += 1
        return index
    except Exception as bug:
        print("Failed to get no of petty cash voucher")
        print(bug)
        return 0


def get_petty_voucher_items(petty_voucher_data: dict, no: int) -> int:
    try:
        voucher_items = []
        total_amount = 0.0
        for index in range(no):
            amount = float(petty_voucher_data.get(f"amount_new{index}"))
            voucher_item = {
                "description": petty_voucher_data.get(f"description_new{index}"),
                "amount": amount,
            }
            voucher_items.append(voucher_item)
            total_amount += amount
        return total_amount, voucher_items
    except Exception as bug:
        print("Failed to get petty voucher items")
        print(bug)
        return 0, []


def add_pettycash_voucher(pettycash_voucher_data: dict) -> bool:
    try:
        with app.app_context():
            payment_made_to = pettycash_voucher_data.get("payment_made_to")
            voucher_no = pettycash_voucher_data.get("voucher_no")
            date_made = pettycash_voucher_data.get("date_made")
            requisition_ref = pettycash_voucher_data.get("requisition_ref")
            reference = generate_reference_number("PettyCashVoucher")
            attachment = save_attachement("PettyCashVoucher", reference)
            description = pettycash_voucher_data.get("description_of_expense")

            no_voucher_items = get_no_petty_cash_voucher(pettycash_voucher_data)
            total_amount, voucher_items = get_petty_voucher_items(
                pettycash_voucher_data, no_voucher_items
            )
            date_made = format_the_date(date_made)
            new_petty_cash_voucher = PettyCashVoucher(
                reference=reference,
                payment_made_to=payment_made_to,
                voucher_no=voucher_no,
                date_created=date_made,
                total_amount=total_amount,
                attachment=attachment,
                voucher_items=json.dumps(voucher_items),
                description_of_expense=description
            )
            new_petty_cash_voucher.requisition = requisition_ref
            new_form = Forms(form_type="PettyCashVoucher", reference=reference)
            db.session.add(new_petty_cash_voucher)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to add petty cash voucher data")
        print(bug)
        return False


def add_refund_note(refund_note_data: dict) -> bool:
    try:
        with app.app_context():
            name = refund_note_data.get("name")
            address = refund_note_data.get("address")
            city = refund_note_data.get("city")
            add_info = refund_note_data.get("add_info")
            original_price = refund_note_data.get("original_price")
            adjusted_price = refund_note_data.get("adjusted_price")
            total_amount = refund_note_data.get("total_amount")
            proforma_invoice_no = refund_note_data.get("proforma_invoice_no")
            proforma_invoice_amount = refund_note_data.get("proforma_invoice_amount")
            reference = generate_reference_number("RefundNote")
            attachment = save_attachement("RefundNote", reference)
            original_price = format_the_price(original_price)
            adjusted_price = format_the_price(adjusted_price)
            total_amount = format_the_price(total_amount)
            proforma_invoice_amount = format_the_price(proforma_invoice_amount)
            description = cash_register_data.get("description_of_expense")

            new_refund_note = RefundNote(
                reference=reference,
                name=name,
                address=address,
                city=city,
                add_info=add_info,
                original_price=original_price,
                adjusted_price=adjusted_price,
                total_amount=total_amount,
                proforma_invoice_no=proforma_invoice_no,
                proforma_invoice_amount=proforma_invoice_amount,
                description_of_expense=description
            )
            new_form = Forms(form_type="RefundNote", reference=reference)
            db.session.add(new_refund_note)
            db.session.add(new_form)
            db.session.commit()
    except Exception as bug:
        print("Failed to add refund note")
        print(bug)
        return False


def load_invoice_numbers():
    try:
        pass
    except Exception as bug:
        print("Failed to load invoice numbers")
        print(bug)
        return False


def add_stock_items(stock_items: dict) -> bool:
    try:
        with app.app_context():
            pass
    except Exception as bug:
        return False


def collect_sales_commision(data):
    commissions = []
    index = 0
    total_amount = 0.0
    while True:
        description = data.get(f"description_new{index}")
        amount = data.get(f"amount_new{index}")
        if not amount or not description:
            break
        amount = format_the_price(amount)
        commission = {"amount": amount, "description": description}
        commissions.append(commission)
        total_amount += amount
        index += 1
    return json.dumps(commissions), total_amount


def add_sales_commission(sale_commission_data: dict) -> bool:
    try:
        with app.app_context():
            name = sale_commission_data.get("name")
            city = sale_commission_data.get("city")
            phone = sale_commission_data.get("phone")
            prepared_by = sale_commission_data.get("prepared_by")
            reference = generate_reference_number("SalesCommission")
            attachment = save_attachement("SalesCommission", reference)
            commissions, total_amount = collect_sales_commision(sale_commission_data)
            amount = format_the_price(total_amount)
            new_sale_commission = SalesCommission(
                reference=reference,
                name=name,
                city=city,
                phone=phone,
                commissions=commissions,
                total_amount=amount,
                attachment=attachment,
                prepared_by=prepared_by,
            )
            new_form = Forms(reference=reference, form_type="SalesCommission")
            db.session.add(new_sale_commission)
            db.session.add(new_form)
            db.session.commit()
            print("New Sale commission added")
            return True
    except Exception as bug:
        print("Failed to add sales commission")
        print(bug)
        return False


def add_quotation_form(quotation_form_data: dict) -> bool:
    try:
        with app.app_context():

            name = quotation_form_data.get("name")
            address = quotation_form_data.get("address")
            city = quotation_form_data.get("city")
            description = quotation_form_data.get("description")
            quotation_date = quotation_form_data.get("quotation_date")
            expiry_date = quotation_form_data.get("expiry_date")
            quotation_no = quotation_form_data.get("quotation_no")
            sales_person = quotation_form_data.get("sales_person")
            amount = quotation_form_data.get("amount")
            tax_collected = quotation_form_data.get("tax_collected")
            prepared_by = quotation_form_data.get("prepared_by")
            reference = generate_reference_number("QuotationForm")
            attachment = save_attachement("QuotationForm", reference)
            description = quotation_form_data.get("description_of_expense")

            quotation_date = format_the_date(quotation_date)
            expiry_date = format_the_date(expiry_date)
            amount = format_the_price(amount)
            tax_collected = format_the_price(tax_collected)

            new_quotation_form = QuatationForm(
                reference=reference,
                name=name,
                address=address,
                city=city,
                attachment=attachment,
                description=description,
                quotation_date=quotation_date,
                expiry_date=expiry_date,
                quotation_no=quotation_no,
                sales_person=sales_person,
                amount=amount,
                tax_collected=tax_collected,
                prepared_by=prepared_by,
                description_of_expense=description
            )
            new_form = Forms(reference=reference, form_type="QuotationForm")
            db.session.add(new_form)
            db.session.add(new_quotation_form)
            db.session.commit()
            print("new Quotation form updated successfully")
            return True
    except Exception as bug:
        print("Failed to add Quotation data")
        print(bug)
        return False


def load_all_stock_items():
    stock_items = StockItems.query.order_by(StockItems.updated_on).all()
    if stock_items:
        return stock_items
    return []


def load_stock_products():
    stock_items = load_all_stock_items()
    items = {}
    for item in stock_items:
        items[item.item_name] = {
            "description": item.item_description,
            "quantity": item.stock_amount,
        }
    return items


@forms_bp.route("/forms", methods=["GET", "POST"])
@login_required
def forms():
    # if request.method == "POST":
    #     return render_template("forms.html", title="Forms", all_forms=load_all_forms())
    return render_template(
        "forms.html",
        title="Forms",
        all_forms=load_all_forms(),
        d_forms=forms_to_be_deleted(),
    )


@forms_bp.route("/forms-viewer")
@login_required
def forms_viewer():
    print("Form viewer has opened.")
    print(f'Can view cash deposit form view {get_current_role().cash_deposit_form_view}')
    print(f'Can view cash register form view {get_current_role().cash_register_form_view}')
    print(f'Can view cash requisition form view {get_current_role().cash_requisition_form_view}')
    print(f"Can view cash retirement form view {get_current_role().cash_retirement_form_view}")
    return render_template("forms-viewer.html", title="Forms", role=get_current_role())


# ============= Forms =============

# Cash Deposit Form
@forms_bp.route("/cash-deposit", methods=["GET", "POST"])
@login_required
def cash_deposit():
    current_user = get_current_role()
    if current_user.cash_deposit_form_view:
        if request.method == "POST":
            add_cash_deposit_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template("forms/cash-deposit.html", title="Forms - Cash Deposit")
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/cash-register", methods=["GET", "POST"])
@login_required
def cash_register():
    current_user = get_current_role()
    if current_user.cash_register_form_view:
        if request.method == "POST":
            add_cash_register_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/cash-register.html", title="Forms - Cash Register"
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/cash-requisition", methods=["GET", "POST"])
@login_required
def cash_requisition():
    current_user = get_current_role()
    if current_user.cash_requisition_form_view:
        if request.method == "POST":
            add_cash_requisition_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/cash-requisition.html",
            title="Forms - Cash Requisition",
            accountant=get_currrent_accountant(),
            admin=get_current_account_admin(),
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/cash-retirement", methods=["GET", "POST"])
@login_required
def cash_retirement():
    current_user = get_current_role()
    if current_user.cash_retirement_form_view:
        if request.method == "POST":
            add_cash_retirement_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/cash-retirement.html", title="Forms - Cash Retirement"
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/claim-form", methods=["GET", "POST"])
@login_required
def claim_form():
    current_user = get_current_role()
    if current_user.claim_form_view:
        if request.method == "POST":
            add_claim_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template("forms/claim-form.html", title="Forms - Claim Form")
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/material-purchase", methods=["GET", "POST"])
@login_required
def material_purchase():
    current_user = get_current_role()
    if current_user.material_purchase_form_view:
        if request.method == "POST":
            add_material_purchase_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/material-purchase.html",
            title="Forms - Material Purchase Form",
            suppliers=load_all_suppliers(),
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/material-requisition", methods=["GET", "POST"])
@login_required
def material_requisition():
    current_user = get_current_role()
    if current_user.material_requisition_form_view:
        if request.method == "POST":
            add_material_requisition_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/material-requisition.html",
            title="Forms - Material Requisition Form",
            list_items=json.dumps(load_stock_products()),
            now=datetime.date.today(),
            items=StockItems.query.order_by(StockItems.date_created.desc()).all(),
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/payment-voucher", methods=["GET", "POST"])
@login_required
def payment_voucher():
    current_user = get_current_role()
    if current_user.payment_voucher_form_view:
        if request.method == "POST":
            add_payment_voucher_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/payment-voucher.html", title="Forms - Payment Voucher Form"
        )
    return redirect(url_for("home_bp._401"))


def get_pvouchers(form):
    current_user = get_current_role()
    if current_user.petty_cash_reconciliation_form_view:
        target_vouchers = []
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        try:
            f_start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
            f_end_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")
            vouchers = PettyCashVoucher.get_rencoliation(f_start_date, f_end_date)
            target_vouchers = vouchers
        except Exception as bug:
            print("Exception raised", bug)
        return render_template(
            "forms/petty-cash-reconciliation.html",
            title="Form - Petty Cash Reconciliation",
            start_date=start_date,
            end_date=end_date,
            target_vouchers=target_vouchers,
            total_amount=sum([p.total_amount for p in target_vouchers]),
        )
    return redirect(url_for("home_bp._401"))


def get_pview_vouchers(reco_data):
    current_user = get_current_role()
    if current_user.petty_cash_reconciliation_form_view:
        target_vouchers = []
        try:
            start_date = reco_data.start_p_date
            end_date = reco_data.end_p_date
            vouchers = PettyCashVoucher.get_rencoliation(start_date, end_date)
            target_vouchers = vouchers
        except Exception as bug:
            print("Exception raised", bug)
        return render_template(
            "view/petty-cash-reconciliation-view.html",
            petty_cash_reco_data=reco_data,
            title="Forms-View - Petty Cash Reconciliation View",
            json=json,
            start_date=start_date,
            end_date=end_date,
            target_vouchers=target_vouchers,
            total_amount=sum([p.total_amount for p in target_vouchers]),
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/petty-cash-reconciliation", methods=["GET", "POST"])
@login_required
def petty_cash_reconciliation():
    current_user = get_current_role()
    if current_user.petty_cash_reconciliation_form_view:
        if request.method == "POST":
            if request.form.get("vouchers"):
                return get_pvouchers(request.form)
            add_PettyCashReconciliation(request.form)
            return redirect(url_for("forms_bp.forms"))

        return render_template(
            "forms/petty-cash-reconciliation.html",
            title="Form - Petty Cash Reconciliation",
            target_vouchers=[],
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/petty-cash-voucher", methods=["GET", "POST"])
@login_required
def petty_cash_voucher():
    current_user = get_current_role()
    if current_user.petty_cash_voucher_form_view:
        if request.method == "POST":
            add_pettycash_voucher(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/petty-cash-voucher.html",
            title="Forms - Petty Cash Voucher",
            requisitions=CashRequisitionForm.query.all(),
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/refund-note", methods=["GET", "POST"])
@login_required
def refund_note():
    current_user = get_current_role()
    if current_user.refund_note_form_view:
        if request.method == "POST":
            add_refund_note(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template("forms/refund-note.html", title="Forms - Refund Note")
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/sales-comission", methods=["GET", "POST"])
@login_required
def sales_comission():
    current_user = get_current_role()
    if current_user.sales_commission_form_view:
        if request.method == "POST":
            add_sales_commission(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/sales-comission.html", title="Forms - Sales Comission"
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/quotation-form", methods=["GET", "POST"])
@login_required
def quotation_form():
    current_user = get_current_role()
    if current_user.quotation_form_view:
        if request.method == "POST":
            add_quotation_form(request.form)
            return redirect(url_for("forms_bp.forms"))
        return render_template(
            "forms/quotation-form.html", title="Forms - Quotation Form"
        )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/actions/<form_type>/<reference>", methods=["GET"])
@login_required
def approve_or_disapprove(form_type: str, reference: str):
    reference = reference.replace("-", "/")
    # -------------GET REQUEST --------------------

    if form_type == "CashDepositForm":
        cash_deposit_data = CashDepositForm.query.filter_by(reference=reference).first()
        return render_template(
            "view/cash-deposit-view.html",
            cash_deposit_data=cash_deposit_data,
            title="Forms-Views - Cash Deposit View",
        )

    elif form_type == "CashRegisterForm":
        cash_register_data = CashRegisterForm.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/cash-register-view.html",
            cash_register_data=cash_register_data,
            title="Forms-Views - Cash Register-View",
        )

    elif form_type == "CashRequisitionForm":
        cash_requisition_data = CashRequisitionForm.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/cash-requisition-view.html",
            cash_requisition_data=cash_requisition_data,
            title="Forms-Views  - Cash Requisition View",
        )

    elif form_type == "CashRetirementForm":
        cash_retirement_data = CashRetirementForm.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/cash-retirement-view.html",
            cash_retirement_data=cash_retirement_data,
            titile="Forms-View  - Cash Retirement View",
            json=json,
        )

    elif form_type == "ClaimForm":
        claim_form_data = ClaimForm.query.filter_by(reference=reference).first()
        return render_template(
            "view/claim-form-view.html",
            claim_form_data=claim_form_data,
            title="Forms-Views - Claim Form View",
            json=json,
        )

    elif form_type == "MaterialPurchaseForm":
        material_purchase_data = MaterialPurchaseForm.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/material-purchase-view.html",
            material_purchase_data=material_purchase_data,
            title="Forms-View - Material Purchase View",
            json=json,
        )

    elif form_type == "MaterialRequisitionForm":
        material_requisition_data = MaterialRequisitionForm.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/material-requisition-view.html",
            material_requisition_data=material_requisition_data,
            title="Forms-View - Material Requisition",
            json=json,
        )

    elif form_type == "PaymentVoucher":
        payment_voucher_data = PaymentVoucher.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/payment-voucher-view.html",
            payment_voucher_data=payment_voucher_data,
            title="Forms-View - Payment Voucher View",
            json=json,
        )

    elif form_type == "PettyCashReconciliation":
        petty_cash_reco_data = PettyCashReconciliation.query.filter_by(
            reference=reference
        ).first()

        return get_pview_vouchers(petty_cash_reco_data)

    elif form_type == "PettyCashVoucher":
        petty_cash_voucher_data = PettyCashVoucher.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/petty-cash-voucher-view.html",
            petty_cash_voucher_data=petty_cash_voucher_data,
            title="Forms-View - Petty Cash Voucher",
            json=json,
        )

    elif form_type == "RefundNote":
        refund_note_data = RefundNote.query.filter_by(reference=reference).first()
        return render_template(
            "view/refund-note-view.html",
            refund_note_data=refund_note_data,
            title="Forms-View - Refund Note",
        )

    elif form_type == "SalesCommission":
        sale_commission_data = SalesCommission.query.filter_by(
            reference=reference
        ).first()
        return render_template(
            "view/sales-commission-view.html",
            sale_commission_data=sale_commission_data,
            title="Forms-View - Sales Commission View",
            json=json,
        )

    elif form_type == "QuotationForm":
        quotation_form_data = QuatationForm.query.filter_by(reference=reference).first()
        return render_template(
            "view/quotation-form-view.html",
            quotation_form_data=quotation_form_data,
            title="Forms-View - Quotation Form View",
        )

    else:
        return {"unknown": "Form name is unknown"}


@forms_bp.route("/form-decision/<reference>/<decision>", methods=["GET"])
@login_required
def form_decision(reference, decision):
    if flask_login.current_user.is_admin:
        reference = reference.replace("-", "/")
        active_form = Forms.query.filter_by(reference=reference).first()
        raw_form = (
            forms_db.get(active_form.form_type)
            .query.filter_by(reference=reference)
            .first()
        )
        decision = decision.strip().capitalize()
        if active_form.form_type == "MaterialPurchaseForm":
            print("stock item added")
            raw_form._status = decision
        else:
            raw_form.status = decision
        active_form.status = decision
        db.session.add(raw_form)
        db.session.add(active_form)
        db.session.commit()
        print(decision)
        print("status changed")
        return redirect(url_for("forms_bp.forms"))
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/stock-items", methods=["GET", "POST"])
@login_required
def stock_items():
    current_role = get_current_role()
    if current_role.stock_items_view:
        if request.method == "GET":
            return render_template(
                "stock-items.html",
                title="Forms - Stock Items",
                stock_items=load_all_stock_items(),
            )
        else:
            return render_template(
                "stock-items.html",
                title="Forms - Stock Items",
                stock_items=load_all_stock_items(),
            )
    return redirect(url_for("home_bp._401"))


@forms_bp.route("/delete-forms/<form_type>/<reference>")
def delete_forms(form_type, reference):
    current_user = flask_login.current_user
    if current_user.is_admin:
        target_form_type = forms_db.get(form_type, None)
        reference = reference.replace("-", "/")
        if target_form_type and reference:
            target_form = target_form_type.query.filter_by(reference=reference).first()
            main_form = Forms.query.filter_by(reference=reference).first()
            if target_form and main_form:
                db.session.delete(main_form)
                db.session.delete(target_form)
                db.session.commit()
                print("Forms has been deleted !!")
                return redirect(url_for("forms_bp.forms"))
    print("Forms Delete Failed")
    return redirect(url_for("forms_bp.forms"))


@forms_bp.route("/delete-form", methods=["POST"])
def delete_form():
    current_user = flask_login.current_user
    form_type = request.form.get("form_type").strip()
    reference = request.form.get("reference")
    reason = request.form.get("reason")
    _form = forms_db.get(form_type, None)
    target_form = _form.query.filter_by(reference=reference).first()
    if not (current_user.is_admin or current_user.role == "adminstrator"):
        if form_type and reference:
            # add to delete list
            forms_to_delete = ItemsToDelete(
                item_id=target_form.form_id,
                table_name=form_type,
                reason=reason,
                requested_by=current_user.email,
            )
            try:
                db.session.add(forms_to_delete)
                db.session.commit()
                print("Forms has beena added to pending delets !!")
            except Exception as bug:
                print(bug)
                db.session.rollback()
    return redirect(url_for("forms_bp.forms"))
