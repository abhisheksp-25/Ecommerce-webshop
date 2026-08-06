#sales_order.py
import frappe
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note
from .supplier_assignment import assign_supplier_to_sales_order




# def validate(doc, method):
    
#     assign_supplier(doc, method)
#     # frappe.throw(frappe.utils.get_url())

# def before_save(doc, mrthod):
#     pass




def assign_supplier(doc, method):
    
    assign_supplier_to_sales_order(doc)

def create_delivery_note(doc, method):
    

    # Sirf submitted Sales Order ke liye
    if doc.docstatus != 1:
        return

    # Agar Delivery Note already ban gaya hai to return
    if frappe.db.exists(
        "Delivery Note Item",
        {"against_sales_order": doc.name}
    ):
        return

    # Delivery Note create karo
    dn = make_delivery_note(doc.name)

    dn.insert(ignore_permissions=True)

    # Direct submit
    dn.submit()

    # frappe.db.commit()