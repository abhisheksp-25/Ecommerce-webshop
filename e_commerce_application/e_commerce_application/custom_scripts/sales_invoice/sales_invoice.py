import frappe
from erpnext.accounts.doctype.payment_entry.payment_entry import get_payment_entry


def create_payment_entry(doc, method):

    # Sirf submitted Sales Invoice ke liye
    if doc.docstatus != 1:
        return

    # Agar Payment Entry already bani hai to return
    if frappe.db.exists(
        "Payment Entry Reference",
        {
            "reference_doctype": "Sales Invoice",
            "reference_name": doc.name
        }
    ):
        return

    # Sales Invoice se Payment Entry banao
    payment_entry = get_payment_entry("Sales Invoice", doc.name)

    # Insert
    payment_entry.insert(ignore_permissions=True)

    # Direct Submit
    payment_entry.submit()

    frappe.db.commit()
    