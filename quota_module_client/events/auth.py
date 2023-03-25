import frappe
from frappe import _
from frappe.utils.data import date_diff, today


def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """
    quota = frappe.db.sql("""SELECT valid_till FROM `tabQ M`""", as_dict=1)

    valid_till = quota[0]['valid_till'] if len(quota) else today()
    diff = date_diff(valid_till, today())

    if diff < 0:
        frappe.throw(_("You site is suspended. Please contact Sales"), frappe.AuthenticationError)
