# user_provisioning.py
"""Creates the Website User linked to a new Supplier Inquiry."""

import frappe

SUPPLIER_PORTAL_ROLE = "Supplier Portal"


def ensure_supplier_portal_role_exists():
    if not frappe.db.exists("Role", SUPPLIER_PORTAL_ROLE):
        role = frappe.new_doc("Role")
        role.role_name = SUPPLIER_PORTAL_ROLE
        role.desk_access = 0
        role.insert(ignore_permissions=True)


def create_website_user(inquiry):
    """Creates (or reuses) a Website User for this inquiry's email."""
    ensure_supplier_portal_role_exists()

    if frappe.db.exists("User", inquiry.email_address):
        return frappe.get_doc("User", inquiry.email_address)

    user = frappe.new_doc("User")
    user.email = inquiry.email_address
    user.first_name = inquiry.first_name
    user.last_name = inquiry.last_name
    user.mobile_no = inquiry.mobile_number
    user.enabled = 1
    user.user_type = "Website User"
    user.send_welcome_email = 0
    user.append("roles", {"role": SUPPLIER_PORTAL_ROLE})

    user.insert(ignore_permissions=True)
    return user