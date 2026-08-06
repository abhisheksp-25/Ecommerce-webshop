import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice


def create_sales_invoice(doc, method):

    # Sirf submitted Delivery Note ke liye
    if doc.docstatus != 1:
        return

    # Agar Sales Invoice already bana hua hai to return
    if frappe.db.exists(
        "Sales Invoice Item",
        {"delivery_note": doc.name}
    ):
        return

    # Delivery Note se Sales Invoice banao
    sales_invoice = make_sales_invoice(doc.name)

    # Insert
    sales_invoice.insert(ignore_permissions=True)

    # Direct Submit
    sales_invoice.submit()

    frappe.db.commit()