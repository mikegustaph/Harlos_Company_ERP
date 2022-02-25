import flask_login
from erp.models.harlos_db import ItemsToDelete
from erp.models.harlos_db import (
    db,
    Users,
    UserRoles,
    ClaimForm,
    ItemsToDelete,
    MaterialPurchaseForm,
    MaterialRequisitionForm,
    PaymentVoucher,
    RefundNote,
    Forms,
    CashDepositForm,
    CashRegisterForm,
    CashRequisitionForm,
    CashRetirementForm,
    PettyCashReconciliation,
    PettyCashVoucher,
    SalesCommission,
    StockItems,
    QuatationForm,
    CustomerContacts,
    Suppliers,
    Leads,
    Container,
    Campaign,
)


# =========================== FORMS CONFIGURATION =========================

extensions = {
    "CashDepositForm": "CDF",
    "CashRegisterForm": "CRGF",
    "CashRequisitionForm": "CRQF",
    "CashRetirementForm": "CRTF",
    "ClaimForm": "CLF",
    "MaterialPurchaseForm": "MPF",
    "MaterialRequisitionForm": "MRF",
    "PaymentVoucher": "PV",
    "PettyCashReconciliation": "PCR",
    "PettyCashVoucher": "PCV",
    "RefundNote": "RN",
    "SalesCommission": "SN",
    "QuotationForm": "QF",
}


forms_db = {
    "CashDepositForm": CashDepositForm,
    "CashRegisterForm": CashRegisterForm,
    "CashRequisitionForm": CashRequisitionForm,
    "CashRetirementForm": CashRetirementForm,
    "ClaimForm": ClaimForm,
    "MaterialPurchaseForm": MaterialPurchaseForm,
    "MaterialRequisitionForm": MaterialRequisitionForm,
    "PaymentVoucher": PaymentVoucher,
    "PettyCashReconciliation": PettyCashReconciliation,
    "PettyCashVoucher": PettyCashVoucher,
    "RefundNote": RefundNote,
    "SalesCommission": SalesCommission,
    "QuotationForm": QuatationForm,
}


raw_path = "erp/static/img/forms/{}"
attachment_paths = {
    "CashDepositForm": raw_path.format("cash_deposit"),
    "CashRegisterForm": raw_path.format("cash_register"),
    "CashRequisitionForm": raw_path.format("cash_requisition"),
    "CashRetirementForm": raw_path.format("cash_retirement"),
    "ClaimForm": raw_path.format("claim_form"),
    "MaterialPurchaseForm": raw_path.format("material_purchase_form"),
    "MaterialRequisitionForm": raw_path.format("material_requisition"),
    "PaymentVoucher": raw_path.format("payment_voucher"),
    "PettyCashReconciliation": raw_path.format("petty_cash_reconciliation"),
    "PettyCashVoucher": raw_path.format("petty_cash_voucher"),
    "RefundNote": raw_path.format("refund_note"),
    "SalesCommission": raw_path.format("sales_commission"),
    "QuotationForm": raw_path.format("quotation"),
}

table_db = {
    "Marketing Contact": CustomerContacts,
    "Suppliers": Suppliers,
    "Lead": Leads,
    "Stock": Container,
    "Campaign": Campaign,
}


# ============================= END OF FORMS CONFIGURATION ======================


def tobe_deleted_items(table_name):
    d_items = ItemsToDelete.query.filter_by(table_name=table_name).all()
    if d_items:
        items_ids = [d_item.item_id for d_item in d_items]
        return items_ids
    return []


def forms_to_be_deleted(table_name: str = "forms") -> list:
    try:
        _target_forms = []
        _forms = ItemsToDelete.query.filter_by().all()
        for _form in _forms:
            if _form.table_name in forms_db:
                _target_form = (
                    forms_db[_form.table_name]
                    .query.filter_by(form_id=_form.item_id)
                    .first()
                )
                _target_forms.append(_target_form.reference)
        return _target_forms

    except Exception as bug:
        print("Failed to get the forms to be deleted")
        print(bug)
        return []


def is_already_added(table_name, item_id):
    item = ItemsToDelete.query.filter(
        (ItemsToDelete.table_name == table_name) & (ItemsToDelete.item_id == item_id)
    ).first()
    return True if item else False


# ====================== FORMS =================================


def get_current_role():
    try:
        role_name = flask_login.current_user.role
        print(role_name)
        return UserRoles.query.filter_by(role_name=role_name).first()
    except Exception as bug:
        print("Failed to get the current role")

        print(bug)
        return None


def format_the_amount(amount: str) -> float:
    try:
        return float("".join(amount.split(",")))
    except Exception as bug:
        print("Failed to format the amount")
        print(bug)
        return False


def create_form_payload(index: int, form: Forms, raw_data) -> dict:
    try:
        return {"index": index, "form": form, "raw_data": raw_data}

    except Exception as bug:
        print("Failed creating form payload")
        print(bug)
        return False


def load_all_forms():
    try:
        structured_forms = []
        all_forms = Forms.query.order_by(Forms.date_created.desc()).all()
        for index, form in enumerate(all_forms):
            if form.form_type == "CashDepositForm":
                raw_data = CashDepositForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "CashRegisterForm":
                raw_data = CashRegisterForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "CashRequisitionForm":
                raw_data = CashRequisitionForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "CashRetirementForm":
                raw_data = CashRetirementForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "ClaimForm":
                raw_data = ClaimForm.query.filter_by(reference=form.reference).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "MaterialPurchaseForm":
                raw_data = MaterialPurchaseForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "MaterialRequisitionForm":
                raw_data = MaterialRequisitionForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "PaymentVoucher":
                raw_data = PaymentVoucher.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "PettyCashReconciliation":
                raw_data = PettyCashReconciliation.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "PettyCashVoucher":
                raw_data = PettyCashVoucher.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            elif form.form_type == "RefundNote":
                raw_data = RefundNote.query.filter_by(reference=form.reference).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "SalesCommission":
                raw_data = SalesCommission.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue

            elif form.form_type == "QuotationForm":
                raw_data = QuatationForm.query.filter_by(
                    reference=form.reference
                ).first()
                payload = create_form_payload(index, form, raw_data)
                structured_forms.append(payload)
                continue
            else:
                print(f"{form.form_type} is probably a typo bug")
                continue
        return structured_forms

    except Exception as bug:
        print("Failed to all_form")
        print(bug)
        return []