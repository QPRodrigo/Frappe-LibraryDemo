# Copyright (c) 2022, QPRodrigo and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryTransaction(Document):
    
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
		    # establecer el estado del artículo para ser Emitido
            article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()

        elif self.type == "Return":
            self.validate_return()
		    # establecer el estado del artículo como Disponible
            article = frappe.get_doc("Article", self.article)
            article.status = "Available"
            article.save()

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
	    # artículo no se puede emitir si ya se emitió
        if article.status == "Issued":
            frappe.throw("El artículo ya ha sido emitido por otro miembro")

    def validate_return(self):
        article = frappe.get_doc("Article", self.article)
	    # artículo no se puede devolver si no se emite primero
        if article.status == "Available":
            frappe.throw("El artículo no se puede devolver sin haber sido emitido primero")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")


    def validate_membership(self):
	    # verificar si existe una membresía válida para este miembro de la biblioteca
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("El miembro no tiene una membresía válida")