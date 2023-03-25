// Copyright (c) 2023, NexTash and contributors
// For license information, please see license.txt

frappe.ui.form.on('License', {
	verify_license: function(frm) {
		frm.call("verify_license")
	}
});
