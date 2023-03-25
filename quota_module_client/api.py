import frappe
import requests
import json

@frappe.whitelist(allow_guest=True)
def verify_license(license_key=None):
    if not license_key:
        return

    doc = frappe.get_doc("License", "License")
    doc.db_set("license_key", license_key, notify=True, commit=True)

    doc.verify_license()
