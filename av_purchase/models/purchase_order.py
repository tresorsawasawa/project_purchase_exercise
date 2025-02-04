from odoo import models, api
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_submit(self):
        """Submit the RFQ logic with additional validations."""
        for order in self:
            # Check if the user is assigned to a department
            if not order.user_id.department_id:
                raise UserError("The user must be assigned to a department in order to submit an RFQ. Please reach out to the system administrator.")
            
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
            department_manager = order.user_id.department_id.manager_id
            if not department_manager:
                raise UserError("The user's department must have a manager assigned to it in order to submit an RFQ. Please reach out to the system administrator.")
            
            # Ensure the department manager has an associated user and belongs to the 'HOD' group
            if not department_manager.user_id or not department_manager.user_id.has_group('av_purchase.group_purchase_hod'):
                raise UserError("The department manager must belong to the 'HOD' group in order to submit an RFQ. Please reach out to the system administrator.")

            # Create a To-Do activity for the HOD when a CP submits an RFQ
            if order.user_id.has_group('av_purchase.group_purchase_cp'):
                if department_manager.user_id:
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                        'res_id': order.id,
                        'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                        'user_id': department_manager.user_id.id,
                        'summary': "RFQ Submitted - Approval Needed",
                        'note': "A new RFQ has been submitted and needs a review or an approval.",
                    })

            # If all validations pass, change the state to 'sent'
            order.write({'state': 'sent'})

        return True
