from odoo import models, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_submit(self):
        """Submit the RFQ logic with additional validations."""
        for order in self:
            # Check if the user is assigned to a department
            if not order.create_uid.employee_id.department_id:
                raise UserError("The RFQ creator must be assigned to a department in order to submit an RFQ. Please reach out to the system administrator.")

            # Ensure that there is at least one order line.
            if not order.order_line:
                raise UserError("The RFQ must contain at least one order line with a Product.")
            
            # Check each order line for valid quantity and price.
            for line in order.order_line:
                if line.product_qty <= 0:
                    raise UserError("The quantity must be greater than 0 for the product '%s'." % (line.product_id.display_name or ''))
                if line.price_unit <= 0:
                    raise UserError("The price must be greater than 0 for the product '%s'." % (line.product_id.display_name or ''))
            
            # Check if the department has a manager
            department_manager = order.create_uid.employee_id.department_id.manager_id
            if not department_manager:
                raise UserError("The RFQ creator's department must have a manager assigned in order to submit an RFQ. Please reach out to the system administrator.")

            # Ensure the department manager has an associated user
            if not department_manager.user_id:
                raise UserError(f"The department manager '{department_manager.name}' does not have an Odoo user account. Please contact the administrator to assign a user account before submitting an RFQ.")

            # If all validations pass, change the state to 'sent'
            order.write({'state': 'sent'})

            # Create a clickable link to the RFQ
            rfq_link = f"<a href='#id={order.id}&model=purchase.order'>{order.name}</a>"

            # Create a To-Do activity for the HOD when a CP submits an RFQ
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'res_id': order.id,
                'res_model_id': self.env.ref('purchase.model_purchase_order').id,
                'user_id': department_manager.user_id.id,
                'summary': f"RFQ To Review",
                'note': f"A new RFQ {rfq_link} has been submitted and needs a review or an approval.",
            })
