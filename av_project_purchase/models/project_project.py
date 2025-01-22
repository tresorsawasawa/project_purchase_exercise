from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_budget = fields.Float(
        string="Project Budget",
        required=True,
        help="Budget allocated for this project."
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for the project budget."
    )
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    department_id = fields.Many2one('hr.department', string='Department')

    @api.constrains("project_budget")
    def _check_project_budget(self):
        for project in self:
            if project.project_budget <= 0:
                raise ValidationError("The project budget must be greater than zero.")
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if not (record.date_start or record.date_end):
                raise ValidationError("Either 'Start Date' or 'End Date' must be provided.")
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError("Start date should precede the end date.")
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError("End date should follow the start date.")

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Automatically set the Project Manager based on the department's manager."""
        if self.department_id:
            self.user_id = self.department_id.manager_id.user_id
        else:
            self.user_id = False
