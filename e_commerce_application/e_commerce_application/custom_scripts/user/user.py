import frappe


def after_insert(doc, method):
    # Sirf Website Users ke liye
    if doc.user_type != "Website User":
        return

    # Agar Customer role already hai to kuch mat karo
    if "Customer" in frappe.get_roles(doc.name):
        return

    user = frappe.get_doc("User", doc.name)

    user.append("roles", {
        "role": "Customer"
    })

    user.save(ignore_permissions=True)
    