# Copyright (c) 2026, Neeraj Ravi Pratap and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document



class HealthcareService(Document):

    def after_insert(self):
        self.create_service_item()

    def create_service_item(self):
        if frappe.db.exists("Item", self.service_name):
            return
        item = frappe.new_doc("Item")
        item.item_code = self.service_name
        item.item_name = self.service_name
        item.description = self.description
        item.is_stock_item = 0
        item.is_sales_item = 1
        item.is_purchase_item = 0
        item.include_item_in_manufacturing = 0
        item.item_group = "Services"
        item.stock_uom = "Nos"
        item.insert(ignore_permissions=True)

        item_price = frappe.new_doc("Item Price")
        item_price.item_code = self.service_name
        item_price.price_list = "Standard Selling"
        item_price.price_list_rate = self.price
        item_price.insert(ignore_permissions=True)