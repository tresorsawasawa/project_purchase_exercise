from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Custom Purchase Order model"
