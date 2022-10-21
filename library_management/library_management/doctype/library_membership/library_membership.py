# Copyright (c) 2022, QPRodrigo and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryMembership(Document):
	# comprobar antes de enviar este documento
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
				#Cuando es Enviado
                "docstatus": DocStatus.submitted(),
                # verificar si la fecha de finalización de la membresía es posterior a la fecha de inicio de esta membresía
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("Hay una membresía activa para este miembro")

		# obtenga el período de préstamo y calcule hasta_fecha agregando período_de_préstamo a fecha_desde_        
        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)