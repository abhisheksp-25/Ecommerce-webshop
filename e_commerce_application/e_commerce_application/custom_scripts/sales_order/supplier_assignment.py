# supplier_assignment.py
"""
Assigns the nearest active Supplier to a Sales Order based on
customer/supplier geolocation, with a "least busy supplier" tie-breaker.

Called from sales_order.py::assign_supplier (Sales Order before_insert hook).
Do not rename any function in this file — other modules depend on these
exact names.
"""

import math

import frappe

from .geolocation import get_coordinates
from .distance import calculate_distance

# Tolerance (in KM) used when comparing distances for a tie.
# Distances are rounded to 2 decimals in distance.py, but comparing floats
# with `==` is still fragile, so we use an explicit tolerance instead.
DISTANCE_TOLERANCE_KM = 0.01


def assign_supplier_to_sales_order(doc):
    """
    Main entry point. Finds the nearest active supplier for the Sales
    Order's customer address and assigns it to
    doc.custom_assigned_supplier.

    Safe to call even if no supplier can be matched — in that case
    custom_assigned_supplier is left unset and a warning is logged,
    so Sales Order creation is never blocked by this step.
    """

    try:
        customer_address = get_customer_address(doc)
        suppliers = get_supplier_list()
        supplier = find_best_supplier(customer_address, suppliers)

        if not supplier:
            frappe.log_error(
                title="Supplier Assignment: No supplier matched",
                message=(
                    f"Sales Order (customer: {doc.customer}, "
                    f"customer_address: {doc.customer_address}) could not "
                    f"be matched to any supplier. Checked {len(suppliers)} "
                    f"active supplier(s)."
                ),
            )
            return

        assign_supplier(doc, supplier)

    except frappe.ValidationError:
        # Deliberate validation failures (e.g. missing customer address)
        # should surface to the user as-is.
        raise
    except Exception:
        # Never let an unexpected error in supplier assignment block
        # Sales Order creation — log it and move on.
        frappe.log_error(
            title="Supplier Assignment: Unexpected error",
            message=frappe.get_traceback(),
        )


def get_customer_address(doc):
    """Return the Address doc linked as the Sales Order's customer_address."""

    if not doc.customer_address:
        frappe.throw("Customer Address is required.")

    return frappe.get_doc("Address", doc.customer_address)


def get_supplier_list():
    """Return all active (non-disabled) suppliers."""

    return frappe.get_all(
        "Supplier",
        filters={"disabled": 0},
        fields=["name", "supplier_name"],
    )


def get_supplier_address(supplier):
    """
    Return the Address doc linked to the given Supplier via Dynamic Link.

    IMPORTANT: Dynamic Link rows are child rows of the Address doctype.
    That means `parenttype` is always "Address" (the doctype the row
    belongs to), never "Supplier". `link_doctype` / `link_name` identify
    what the address is linked TO. Filtering on parenttype="Supplier"
    (as the previous implementation did) will never match a row, which
    was the root cause of suppliers never being found.
    """

    linked_address = frappe.get_all(
        "Dynamic Link",
        filters={
            "link_doctype": "Supplier",
            "link_name": supplier,
            "parenttype": "Address",
        },
        fields=["parent"],
        limit=1,
    )

    if not linked_address:
        return None

    return frappe.get_doc("Address", linked_address[0].parent)


def find_best_supplier(customer_address, suppliers):
    """
    Compute distance from the customer to every active supplier and
    return the name of the nearest one. Ties are broken by choosing the
    supplier with the fewest completed (submitted) Sales Orders.
    """

    customer_lat, customer_lon = get_coordinates(customer_address)

    if customer_lat is None or customer_lon is None:
        frappe.throw("Customer geolocation is missing.")

    supplier_distances = []

    for supplier in suppliers:
        supplier_address = get_supplier_address(supplier.name)

        if not supplier_address:
            frappe.logger().warning(
                f"Supplier Assignment: no linked address found for "
                f"supplier {supplier.name}, skipping."
            )
            continue

        supplier_lat, supplier_lon = get_coordinates(supplier_address)

        if supplier_lat is None or supplier_lon is None:
            frappe.logger().warning(
                f"Supplier Assignment: supplier {supplier.name} has an "
                f"address but no valid geolocation, skipping."
            )
            continue

        distance = calculate_distance(
            customer_lat, customer_lon, supplier_lat, supplier_lon
        )

        supplier_distances.append({
            "supplier": supplier.name,
            "distance": distance,
        })

    if not supplier_distances:
        return None

    minimum_distance = min(item["distance"] for item in supplier_distances)

    nearest_suppliers = [
        item["supplier"]
        for item in supplier_distances
        if math.isclose(item["distance"], minimum_distance, abs_tol=DISTANCE_TOLERANCE_KM)
    ]

    if len(nearest_suppliers) == 1:
        return nearest_suppliers[0]

    # Tie -> least busy supplier
    supplier_objects = [frappe._dict({"name": name}) for name in nearest_suppliers]
    return get_least_busy_supplier(supplier_objects)


def get_least_busy_supplier(suppliers):
    """Among a list of tied suppliers, return the one with the fewest
    completed (submitted) Sales Orders."""

    selected_supplier = None
    least_orders = None

    for supplier in suppliers:
        order_count = frappe.db.count(
            "Sales Order",
            filters={
                "custom_assigned_supplier": supplier.name,
                "docstatus": 1,
            },
        )

        if least_orders is None or order_count < least_orders:
            least_orders = order_count
            selected_supplier = supplier.name

    return selected_supplier


def assign_supplier(doc, supplier):
    """Set the resolved supplier on the Sales Order."""

    if not supplier:
        return

    doc.custom_assigned_supplier = supplier