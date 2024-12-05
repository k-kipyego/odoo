# wizard/xmlrpc_operations_wizard.py
from odoo import models, fields, api
from odoo.exceptions import UserError


class XMLRPCOperationsWizard(models.TransientModel):
    _name = 'xmlrpc.operations.wizard'
    _description = 'XML-RPC Operations Wizard'

    connection_id = fields.Many2one('xmlrpc.connection', string='Connection', required=True)
    operation = fields.Selection([
        ('create_sale_order', 'Create Sale Order'),
        ('create_invoice', 'Create Invoice'),
        ('update_stock', 'Update Stock'),
        ('get_product_info', 'Get Product Information')
    ], string='Operation', required=True)

    def action_execute(self):
        self.ensure_one()

        if self.operation == 'create_sale_order':
            return self._create_sale_order()
        elif self.operation == 'create_invoice':
            return self._create_invoice()
        # Add more operations as needed

    def _create_sale_order(self):
        handler = self.env['xmlrpc.handler'].create({
            'connection_id': self.connection_id.id,
            'model_name': 'sale.order',
            'operation': 'create',
            'values': '''{
                'partner_id': 1,
                'order_line': [
                    (0, 0, {
                        'product_id': 1,
                        'product_uom_qty': 1
                    })
                ]
            }'''
        })
        return handler.action_execute()