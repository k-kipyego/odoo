# models/xmlrpc_log.py
from odoo import models, fields


class XMLRPCLog(models.Model):
    _name = 'xmlrpc.log'
    _description = 'XML-RPC Operation Log'
    _order = 'create_date desc'

    handler_id = fields.Many2one('xmlrpc.handler', string='Operation', required=True)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    execution_time = fields.Float('Execution Time (s)')
    result = fields.Text('Result')

    model_name = fields.Char(related='handler_id.model_name')
    operation = fields.Selection(related='handler_id.operation')