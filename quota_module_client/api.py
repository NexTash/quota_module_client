import frappe

@frappe.whitelist(allow_guest=True)
def verify_license(license_key=None):
    if not license_key:
        return
        
    doc = frappe.get_doc("License", "License")
    doc.license_key = license_key
    doc.save(ignore_permissions=True)

    doc.verify_license()