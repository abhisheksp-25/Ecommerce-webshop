# supplier_inquiry.py
"""
Hook target for Supplier Inquiry: after_insert
(wired in hooks.py in the next step)
"""

import frappe
from .user_provisioning import create_website_user
from .registration_token import generate_token


def process_new_inquiry(doc, method):

    

    try:
        user = create_website_user(doc)
        doc.created_user = user.name

        raw_token, expires_on = generate_token()
        doc.registration_token = raw_token
        doc.token_expires_on = expires_on
        doc.email_sent = 1
        doc.status = "Email Sent"

        # save() (not db_set) so the built-in Notification's
        # "Value Change" trigger on registration_token actually fires.
        doc.save(ignore_permissions=True)

    except Exception:
        doc.db_set("status", "Email Failed")
        frappe.log_error(
            title="Supplier Inquiry: onboarding failed",
            message=frappe.get_traceback(),
        )