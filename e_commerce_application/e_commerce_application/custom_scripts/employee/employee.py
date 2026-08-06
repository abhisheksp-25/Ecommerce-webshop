import frappe
import os
import shutil
from .qr_code import generate_employee_qr

def validate(doc,method):
    rename_documents(doc)
    
def rename_documents(doc):
    rename_file(doc, "custom_aadhar_card", "aadhar")
    rename_file(doc, "custom_pan", "pan")


def rename_file(doc, fieldname, prefix):

    file_url = doc.get(fieldname)

    if not file_url:
        return

    files = frappe.get_all(
        "File",
        filters={"file_url": file_url},
        fields=["name", "file_name", "file_url", "is_private"],
        limit=1
    )

    if not files:
        return

    file_doc = frappe.get_doc("File", files[0].name)

    ext = os.path.splitext(file_doc.file_name)[1]
    new_filename = f"{prefix}_{doc.employee}_{doc.first_name}{ext}"

    if file_doc.file_name == new_filename:
        return

    old_path = frappe.get_site_path(file_doc.file_url.lstrip("/"))

    if file_doc.is_private:
        new_url = f"/private/files/{new_filename}"
    else:
        new_url = f"/files/{new_filename}"

    new_path = frappe.get_site_path(new_url.lstrip("/"))

    if os.path.exists(old_path):
        shutil.move(old_path, new_path)

    file_doc.file_name = new_filename
    file_doc.file_url = new_url
    file_doc.save(ignore_permissions=True)

    doc.db_set(fieldname, new_url)

def after_save(doc, method):
   generate_employee_qr(doc)


