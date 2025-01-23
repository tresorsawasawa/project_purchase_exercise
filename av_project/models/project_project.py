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

    def _validate_project_budget(self, budget):
        """Ensure project budget is not negative."""
        if budget < 0:
            raise ValidationError("The project budget must not be negative.")

    def _set_user_from_department(self, vals):
        """Set user_id based on department's manager."""
        department_id = vals.get('department_id')
        if department_id:
            department = self.env['hr.department'].browse(department_id)
            if department.manager_id and department.manager_id.user_id:
                vals['user_id'] = department.manager_id.user_id.id
            else:
                raise ValidationError(
                    f"The manager for the department '{department.name}' does not have a linked user. "
                    f"Please ensure the manager is correctly configured."
                )

    @api.model
    def create(self, vals):
        """Ensure project_budget is not negative and set user_id from department."""
        # Validate project_budget
        self._validate_project_budget(vals.get("project_budget", 0))

        # Set user_id from department manager
        self._set_user_from_department(vals)

        return super().create(vals)

    def write(self, vals):
        """Ensure project_budget is not negative and set user_id if department changes."""
        for project in self:
            # Validate project_budget if updated
            if 'project_budget' in vals:
                self._validate_project_budget(vals.get("project_budget", project.project_budget))

            # Set user_id if department_id changes
            if 'department_id' in vals:
                self._set_user_from_department(vals)

        return super().write(vals)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Set the Project Manager based on the department's manager."""
        for record in self:
            if record.department_id:
                if not record.department_id.manager_id or not record.department_id.manager_id.user_id:
                    raise ValidationError(
                        f"The manager for the department '{record.department_id.name}' does not have a linked user. "
                        f"Please ensure the manager is correctly configured."
                    )
                record.user_id = record.department_id.manager_id.user_id
            else:
                record.user_id = False
