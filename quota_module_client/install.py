import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, today


def before_install():
    # Create Table
    frappe.db.sql(
        f"""
			CREATE TABLE if not exists `tabQ M`
            (`id` INT DEFAULT 0,
            `users` INT DEFAULT 1,
            `active_users` INT DEFAULT 0,
            `space` INT DEFAULT 0,
            `db_space` INT DEFAULT 0,
            `company` INT DEFAULT 1,
            `used_company` INT DEFAULT 1,
            `count_website_users` INT DEFAULT 0,
            `count_administrator_user` INT DEFAULT 1,
            `valid_till` datetime(6),
            PRIMARY KEY (`id`))
			"""
    )
    
    # Count Active Users
    active_users = frappe.db.sql("""SELECT COUNT(DISTINCT `tabUser`.name) as active_users 
    FROM ((`tabUser` 
    INNER JOIN `tabHas Role` ON `tabUser`.name = `tabHas Role`.parent) 
    INNER JOIN `tabRole` ON `tabRole`.name = `tabHas Role`.role)    
    WHERE `tabUser`.enabled = 1 AND `tabRole`.desk_access = 1 AND `tabUser`.name NOT IN ('Guest', 'Administrator')
    """, as_dict=1)
    
    active_users = active_users[0].active_users if len(active_users) else 0
    valid_till = add_days(today(), 14)

    # Updating Data
    frappe.db.sql(f"""INSERT INTO `tabQ M` VALUES (1, 5, {active_users}, 0, 0, 2, 1, 0, 0, '{valid_till}')""")
