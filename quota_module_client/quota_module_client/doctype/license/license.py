# Copyright (c) 2023, NexTash and contributors
# For license information, please see license.txt

import frappe
import requests
import json
from frappe.model.document import Document


class License(Document):
    @frappe.whitelist()
    def verify_license(self):

        # Set the API endpoint URL
        url = "http://127.0.0.1:8000/api/method/quota_module_controller.api.verify_license"
        data = {'license_key': self.license_key}

        # Make the API request and store the response in a variable
        response = requests.get(url, data=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            data = json.loads(response.content)
            data = data.get('message')
            if data.get("verification"):
                frappe.msgprint(f"License key verified!")
                # Updating Data
                d = data
                frappe.db.sql(f"""UPDATE `tabQ M` SET users={d.get('users')}, space={d.get('space')}, db_space={d.get('db_space')}, company={d.get('company')}, valid_till = '{d.get("valid_till")}'""")
            else:
                frappe.throw(f"License key not verified!")
        else:
            # Print an error message if the request failed
            frappe.throw(
                f"Error {response.status_code}: {response.json()['message']}")
