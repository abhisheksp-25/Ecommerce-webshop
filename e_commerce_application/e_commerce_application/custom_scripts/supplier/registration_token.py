# registration_token.py
"""
Simple token generation/verification for the supplier registration link.
Token is stored as-is on Supplier Inquiry.registration_token so that
the built-in Notification feature can embed it directly in the email
link using Jinja: {{ doc.registration_token }}
"""

import secrets
import frappe
from frappe.utils import now_datetime, add_to_date, get_datetime

TOKEN_VALIDITY_HOURS = 72


def generate_token():
    """Returns (token, expires_on)"""
    token = secrets.token_urlsafe(24)
    expires_on = add_to_date(now_datetime(), hours=TOKEN_VALIDITY_HOURS)
    return token, expires_on


def verify_token(token):
    """
    Returns the Supplier Inquiry doc if the token is valid, unused,
    and not expired. Otherwise returns None.
    """
    if not token:
        return None

    inquiry_name = frappe.db.get_value(
        "Supplier Inquiry",
        {"registration_token": token},
        "name",
    )

    if not inquiry_name:
        return None

    inquiry = frappe.get_doc("Supplier Inquiry", inquiry_name)

    if inquiry.registration_completed:
        return None

    if not inquiry.token_expires_on or get_datetime(inquiry.token_expires_on) < now_datetime():
        return None

    return inquiry


def consume_token(inquiry):
    """Marks the token as used so the same email link can't be reused."""
    inquiry.db_set("registration_completed", 1)