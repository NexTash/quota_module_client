import frappe

@frappe.whitelist()
def update_quota():
    d = {
        'users': 5,
        'space': 0,
        'db_space': 0,
        'company': 2,
        'valid_till': add_days(today(), 14)
    }

    # Updating Data
    frappe.db.sql(
        f"""UPDATE `tabQ M` SET users={d.users}, space={d.space}, db_space={d.db_space}, company={company}, valid_till = '{valid_till}')""")
