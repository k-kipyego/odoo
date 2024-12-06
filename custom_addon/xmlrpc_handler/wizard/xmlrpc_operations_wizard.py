from odoo import models, fields, api
from odoo.exceptions import UserError


class XMLRPCOperationsWizard(models.TransientModel):
    _name = 'xmlrpc.operations.wizard'
    _description = 'XML-RPC Operations Wizard'

    operation = fields.Selection([
        ('create_sale_order', 'Create Sale Order'),
        ('create_invoice', 'Create Invoice'),
        ('update_stock', 'Update Stock'),
        ('get_product_info', 'Get Product Information')
    ], string='Operation', required=True)

    def action_execute(self):
        self.ensure_one()

        try:
            # Map operation to appropriate method
            if self.operation == 'create_sale_order':
                handler = self._create_sale_order()
            elif self.operation == 'create_invoice':
                handler = self._create_invoice()
            elif self.operation == 'update_stock':
                handler = self._update_stock()
            elif self.operation == 'get_product_info':
                handler = self._get_product_info()
            else:
                raise UserError("Invalid operation selected")

            # Execute and handle response
            handler.action_execute()
            
            if handler.state == 'failed':
                raise UserError(handler.error_message or "Operation failed")
            
            # Show result in a form view
            return {
                'name': f'Result: {handler.name}',
                'type': 'ir.actions.act_window',
                'res_model': 'xmlrpc.handler',
                'res_id': handler.id,
                'view_mode': 'form',
                'target': 'new',
            }

        except Exception as e:
            raise UserError(str(e))

    def _create_sale_order(self):
        """Create a sale order through the XMLRPC handler."""
        return self.env['xmlrpc.handler'].create({
            'name': 'Create Sale Order',
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

    def _create_invoice(self):
        """Create an invoice through XMLRPC."""
        return self.env['xmlrpc.handler'].create({
            'name': 'Create Invoice',
            'model_name': 'account.move',
            'operation': 'create',
            'values': '''{
                'partner_id': 1,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': 1,
                        'quantity': 1,
                        'price_unit': 100
                    })
                ]
            }'''
        })

    def _update_stock(self):
        """Update stock through XMLRPC."""
        return self.env['xmlrpc.handler'].create({
            'name': 'Update Stock',
            'model_name': 'stock.quant',
            'operation': 'write',
            'domain': '[["product_id", "=", 1]]',
            'values': '''{
                'quantity': 100
            }'''
        })

    def _get_product_info(self):
        """Fetch product information through the XMLRPC handler."""
        return self.env['xmlrpc.handler'].create({
            'name': 'Get Product Info',
            'model_name': 'product.product',
            'operation': 'read',
            'ids_list': '[1]',
            'fields_list': '["name", "lst_price", "qty_available"]'
        })