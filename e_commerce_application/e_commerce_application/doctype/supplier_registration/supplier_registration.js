// Copyright (c) 2026, abhishekspatil90@gmail.com and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Supplier Registration", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Supplier Registration", {
    refresh(frm) {

        if (!frm.is_new() && !frm.doc.created_supplier) {

            frm.add_custom_button("Create Supplier", function () {

                frappe.call({
                    method: "e_commerce_application.e_commerce_application.custom_scripts.supplier.supplier_provisioning.create_supplier_from_registration",
                    args: {
                        registration_name: frm.doc.name
                    },
                    callback: function(r) {

                        if (!r.exc) {
                            frappe.msgprint("Supplier created successfully.");
                            frm.reload_doc();
                        }

                    }
                });

            });

        }

    }
});