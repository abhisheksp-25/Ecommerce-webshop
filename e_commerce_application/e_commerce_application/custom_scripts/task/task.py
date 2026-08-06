import frappe
from frappe.utils.file_manager import save_file


def validate(doc, method):

    # Run only when Task is Completed
    if doc.status != "Completed":
        return
    print("---------------status completed",doc.status)
    if not doc.project:
        return

    project = frappe.get_doc("Project", doc.project)
    print("----------------------------->",project)
    if not project.project_name:
        return
    print("----------------------------->",project.project_name)

    if "Employee Separation" not in project.project_name:
        return
    print("----------------------------->",project.project_name)

    employee = project.project_name.split(":")[-1].strip()
    print("----------------------------->",employee)

    # Find Employee Separation
    separation_name = frappe.db.get_value(
        "Employee Separation",
        {
            "employee": employee,
            "docstatus": 1,
            "boarding_status": "Completed"
        },
        "name"
    )
    print("---------------------------------->",separation_name)

    if not separation_name:
        frappe.msgprint("Employee Separation Not Found")
        return
    print("----------------------------->",separation_name)

    # Generate PDF
    # try:
    pdf = frappe.get_print(
        "Employee Separation",
        separation_name,
        as_pdf=True
    )
    
    # except Exception:
    #     frappe.log_error(
    #         title="Employee Separation PDF Error",
    #         message=frappe.get_traceback()
    #     )
    #     frappe.throw("Unable to Generate Employee Separation PDF")

    filename = f"Resignation_{employee}.pdf"


    # Save PDF as File
    file_doc = save_file(
        fname=filename,
        content=pdf,
        dt="Employee",
        dn=employee,
        is_private=1,
    )
    print("----------------------------->",file_doc)
 
    
    frappe.db.set_value(
        "Employee",
        employee,
        "custom_resignation_format",
        file_doc.file_url
    )
    

    frappe.db.commit()

    frappe.msgprint("Resignation PDF Attached Successfully")