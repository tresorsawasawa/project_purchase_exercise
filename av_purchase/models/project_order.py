from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectOrder(models.Model):
    _inherit = "project.order"

