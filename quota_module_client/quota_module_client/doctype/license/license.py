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
            d = json.loads(response.content)
            d = d.get('message')
            if d.get("verification"):
                # Updating Data
                frappe.db.sql(f"""UPDATE `tabQ M` SET users={d.get('users')}, space={d.get('space')}, db_space={d.get('db_space')}, company={d.get('company')}, valid_till = '{d.get("valid_till")}'""")
                self.db_set("is_varified", 1, notify=True, commit=True)
                return 1
            else:
                self.db_set("is_varified", 1, notify=True, commit=True)
                return 0
        else:
            # Print an error message if the request failed
            frappe.throw(
                f"Error {response.status_code}: {response.json()['message']}")
        return 0