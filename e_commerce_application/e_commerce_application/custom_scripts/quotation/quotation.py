import frappe
from erpnext.selling.doctype.quotation.quotation import make_sales_order


def create_sales_order(doc, method):
    print("triger============>")
    # Safety check
    if doc.docstatus != 1:
        return
    print("doc name-------------_>",doc.name)
    # Agar Sales Order already bana hai to dubara mat banao
    # if frappe.db.exists("Sales Order", {"quotation": doc.name}):
    #     return

    # Sales Order create karo
    sales_order = make_sales_order(doc.name)

    sales_order.insert(ignore_permissions=True)
    print("sales_order==============+>",sales_order.name)

    # Agar direct submit karna hai
    sales_order.submit()

    frappe.db.commit()