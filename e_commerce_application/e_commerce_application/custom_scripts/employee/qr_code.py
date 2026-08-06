import frappe
import qrcode
from io import BytesIO
from frappe.utils.file_manager import save_file


def generate_employee_qr(doc):

    vcard = f"""BEGIN:VCARD
VERSION:3.0
N:{doc.employee_name}
FN:{doc.employee_name}
ORG:{doc.company or ''}
TITLE:{doc.designation or ''}
TEL;TYPE=CELL:{doc.cell_number or ''}
EMAIL:{doc.company_email or doc.personal_email or ''}
END:VCARD"""

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )

    qr.add_data(vcard)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    file_name = f"qr_{doc.name}.png"

    # Delete old QR if present
    existing = frappe.db.get_value(
        "File",
        {
            "attached_to_doctype": "Employee",
            "attached_to_name": doc.name,
            "attached_to_field": "custom_id_card_qr_code",
        },
        "name",
    )

    if existing:
        frappe.delete_doc(
            "File",
            existing,
            ignore_permissions=True,
            force=True,
        )

    saved = save_file(
        fname=file_name,
        content=buffer.getvalue(),
        dt="Employee",
        dn=doc.name,
        df="custom_id_card_qr_code",
        is_private=0,
    )

    frappe.db.set_value(
        "Employee",
        doc.name,
        "custom_id_card_qr_code",
        saved.file_url,
        update_modified=False,
        
    )