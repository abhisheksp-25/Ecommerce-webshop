"""
Admin ke "Create Supplier" button se call hota hai.
Address create hote hi EXISTING Address validate hook
(geocoding.update_geolocation) apne aap fire hoga.
"""

import frappe


@frappe.whitelist()
def create_supplier_from_registration(registration_name):

    registration = frappe.get_doc("Supplier Registration", registration_name)

    # Supplier already created
    if registration.created_supplier:
        frappe.msgprint(
            f"Supplier already created: {registration.created_supplier}"
        )
        return registration.created_supplier

    # ---------------------------
    # Create Supplier
    # ---------------------------

    supplier = frappe.new_doc("Supplier")
    supplier.supplier_name = registration.supplier_display_name
    supplier.supplier_group = registration.supplier_category
    supplier.supplier_type = "Company"
    supplier.country = registration.country
    supplier.tax_id = registration.gst_number

    supplier.insert(ignore_permissions=True)

    # ---------------------------
    # Create Address
    # Existing Address.validate hook
    # will automatically generate geolocation
    # ---------------------------

    address = frappe.new_doc("Address")
    address.address_title = registration.company_name
    address.address_type = "Billing"
    address.address_line1 = registration.address_line_1
    address.address_line2 = registration.address_line_2
    address.city = registration.city
    address.state = registration.state
    address.country = registration.country
    address.pincode = registration.pin_code

    address.append(
        "links",
        {
            "link_doctype": "Supplier",
            "link_name": supplier.name,
        }
    )

    address.insert(ignore_permissions=True)

    # ---------------------------
    # Create Contact
    # ---------------------------

    contact = frappe.new_doc("Contact")

    contact.first_name = (
        registration.primary_contact_name
        or registration.supplier_display_name
    )

    if registration.primary_contact_number:
        contact.append(
            "phone_nos",
            {
                "phone": registration.primary_contact_number,
                "is_primary_phone": 1,
            },
        )

    if registration.primary_contact_email:
        contact.append(
            "email_ids",
            {
                "email_id": registration.primary_contact_email,
                "is_primary": 1,
            },
        )

    contact.append(
        "links",
        {
            "link_doctype": "Supplier",
            "link_name": supplier.name,
        },
    )

    contact.insert(ignore_permissions=True)

    # ---------------------------
    # Update Supplier Registration
    # ---------------------------

    registration.db_set("created_supplier", supplier.name)
    registration.db_set("created_address", address.name)
    registration.db_set("created_contact", contact.name)
    registration.db_set("status", "Supplier Created")

    # ---------------------------
    # Update Supplier Inquiry
    # ---------------------------

    inquiry = frappe.get_doc(
        "Supplier Inquiry",
        registration.supplier_inquiry,
    )

    inquiry.db_set("created_supplier", supplier.name)
    inquiry.db_set("status", "Registration Completed")

    frappe.sendmail(
    recipients=[registration.custom_email_address],
    subject="Supplier Registration Approved",
    message=f"""
    <p>Dear {registration.supplier_display_name},</p>

    <p>Congratulations!</p>

    <p>Your supplier registration has been approved successfully.</p>

    <p>You are now an approved supplier in our E Commerce Application system.</p>

    <p>Regards,<br>{frappe.defaults.get_global_default("company")}</p>
    """
    )

    frappe.db.commit()

    frappe.msgprint(
        f"Supplier <b>{supplier.name}</b> created successfully."
    )

    return supplier.name