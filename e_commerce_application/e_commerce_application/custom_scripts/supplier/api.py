# api.py
import frappe
from .registration_token import verify_token
from .supplier_provisioning import create_supplier_from_registration


@frappe.whitelist(allow_guest=True)
def check_registration_token(token):
    """Web Form client script isko call karega token check karne ke liye."""
    inquiry = verify_token(token)
    if not inquiry:
        return {"valid": False}
    return {"valid": True, "company_name": inquiry.company_name}


@frappe.whitelist()
def create_supplier(registration_name):
    """Admin ke 'Create Supplier' button se call hota hai."""
    frappe.only_for(("System Manager", "Purchase Manager"))
    return create_supplier_from_registration(registration_name)