import subprocess

import frappe
from frappe.installer import update_site_config
from frappe.utils.data import add_days, today


def before_install():
    frappe.db.sql(f"""DROP TABLE if exists `tabQ M`""")

    # Create Table
    frappe.db.sql(
        f"""
			CREATE TABLE if not exists `tabQ M`
            (`id` INT DEFAULT 0,
            `users` INT DEFAULT 1,
            `active_users` INT DEFAULT 0,
            `space` INT DEFAULT 0,
            `used_space` INT DEFAULT 0,
            `private_files_size` INT DEFAULT 0,
            `public_files_size` INT DEFAULT 0,
            `backup_files_size` INT DEFAULT 0,
            `db_space` INT DEFAULT 0,
            `used_db_space` INT DEFAULT 0,
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
    # all possible file locations

    site_path = frappe.get_site_path()
    private_files_path = site_path + '/private/files'
    public_files_path = site_path + '/public/files'
    backup_files_path = site_path + '/private/backups'

    # Calculating Sizes
    total_size = get_directory_size(site_path)
    private_files_size = get_directory_size(private_files_path)
    public_files_size = get_directory_size(public_files_path)
    backup_files_size = get_directory_size(backup_files_path)

    # Getting DB Space
    used_db_space = frappe.db.sql(
        '''SELECT `table_schema` as `database_name`, SUM(`data_length` + `index_length`) / 1024 / 1024 AS `database_size` FROM information_schema.tables  GROUP BY `table_schema`''')[1][1]
    used_db_space = int(used_db_space)
    total_company = len(frappe.db.get_all('Company', filters={}))
    
    # Updating Data
    frappe.db.sql(
        f"""INSERT INTO `tabQ M` VALUES (1, 5, {active_users}, 0, {total_size}, {private_files_size}, {public_files_size}, {backup_files_size}, 0, {used_db_space}, 5, {total_company}, 0, 0, '{valid_till}')""")


# Directory Size
def get_directory_size(path):
    '''
    returns total size of directory in MBss
    '''
    output_string = subprocess.check_output(["du", "-mcs", "{}".format(path)])
    total_size = ''
    for char in output_string:
        if chr(char) == "\t":
            break
        else:
            total_size += chr(char)

    return int(total_size)
