from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectProject(models.Model):
    _inherit = "project.project"

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        help="Currency used for the project budget."
    )

    project_budget = fields.Float(
        string="Project Budget",
        required=True,
        help="Budget allocated for this project."
    )

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True
    )
    user_id = fields.Many2one('res.users', default=False, tracking=True, compute="_compute_user_id")
    date_start = fields.Date(tracking=True, required=True)
    date = fields.Date(required=True)

    def _validate_project_budget(self, budget):
        """Ensure project budget is not negative."""
        if budget < 0:
            raise ValidationError("The project budget must not be negative.")

    @api.depends('department_id')
    def _compute_user_id(self):
       for record in self:
            if record.department_id:
                if not record.department_id.manager_id or not record.denMpartment_id.manager_id.user_id:
                    raise ValidationError(
                        f"The manager for the department '{record.department_id.name}' does not have a linked user. "
                        f"Please ensure the manager is correctly configured."
                    )
                record.user_id = record.department_id.manager_id.user_id
            else:
                record.user_id = False

    @api.model
    def create(self, vals):
        """Ensure project_budget is not negative."""
        # Validate project_budget
        self._validate_project_budget(vals.get("project_budget", 0))

        return super().create(vals)

    def write(self, vals):
        """Ensure project_budget is not negative."""
        for project in self:
            # Validate project_budget if updated
            if 'project_budget' in vals:
                self._validate_project_budget(vals.get("project_budget", project.project_budget))

        return super().write(vals)

