# supplier_registration.py
"""Hook targets for Supplier Registration: before_insert + after_insert"""

import frappe
from .registration_token import verify_token, consume_token


def validate_registration_token(doc, method):
    """before_insert — sirf verify karo, consume mat karo yaha."""
    inquiry = verify_token(doc.registration_token)

    if not inquiry:
        frappe.throw(
            "This registration link is invalid or has expired. Please contact us for a new link.",
            title="Registration Link Expired",
        )

    if frappe.db.exists("Supplier Registration", {"supplier_inquiry": inquiry.name}):
        frappe.throw("A registration has already been submitted for this inquiry.")

    doc.supplier_inquiry = inquiry.name
    doc.custom_email_address = inquiry.email_address


def mark_token_consumed(doc, method):
    """after_insert — ab document safely ban chuka hai, token consume karo."""
    inquiry = frappe.get_doc("Supplier Inquiry", doc.supplier_inquiry)
    consume_token(inquiry)