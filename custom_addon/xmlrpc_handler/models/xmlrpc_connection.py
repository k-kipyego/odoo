# models/xmlrpc_connection.py
from odoo import models, fields, api
import xmlrpc.client

class XMLRPCConnection(models.Model):
    _name = 'xmlrpc.connection'
    _description = 'XML-RPC Connection'

    name = fields.Char('Name', required=True)
    url = fields.Char('Server URL', required=True, default='http://localhost:8069')
    database = fields.Char('Database Name', required=True)
    username = fields.Char('Username', required=True)
    password = fields.Char('Password', required=True)
    active = fields.Boolean('Active', default=True)

    def test_connection(self):
        self.ensure_one()
        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            uid = common.authenticate(self.database, self.username, self.password, {})
            if uid:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'message': 'Connection successful!',
                        'type': 'success',
                        'sticky': False,
                    }
                }
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'Authentication failed',
                    'type': 'danger',
                    'sticky': False,
                }
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': f'Connection failed: {str(e)}',
                    'type': 'danger',
                    'sticky': False,
                }
            }