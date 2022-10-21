// Copyright (c) 2022, QPRodrigo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Library Member', {
    refresh: function(frm) {
        frm.add_custom_button('Crear membresía', () => {
            frappe.new_doc('Library Membership', {
                library_member: frm.doc.name
            })
        })
        frm.add_custom_button('Transacción de biblioteca', () => {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            })
        })
    }
});