# models/xmlrpc_handler.py
from odoo import models, fields, api
import xmlrpc.client
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class XMLRPCHandler(models.Model):
    _name = 'xmlrpc.handler'
    _description = 'XML-RPC Operation Handler'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    connection_id = fields.Many2one('xmlrpc.connection', string='Connection',
                                    required=True)
    model_name = fields.Char(string='Model Name', required=True, tracking=True)
    operation = fields.Selection([
        ('execute', 'Execute Method'),
        ('search', 'Search'),
        ('read', 'Read'),
        ('search_read', 'Search & Read'),
        ('create', 'Create'),
        ('write', 'Write'),
        ('unlink', 'Unlink')
    ], string='Operation', required=True, tracking=True)

    domain = fields.Text('Search Domain', help='Python list/tuple expression')
    fields_list = fields.Text('Fields List', help='Python list of fields')
    values = fields.Text('Values', help='Python dictionary for create/write')
    ids_list = fields.Text('Record IDs', help='Python list of IDs')
    method_name = fields.Char('Method Name', help='Custom method to execute')
    method_args = fields.Text('Method Arguments', help='Python list of arguments')
    method_kwargs = fields.Text('Method Keyword Args', help='Python dict of keyword arguments')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('failed', 'Failed')
    ], string='Status', default='draft', tracking=True)

    result = fields.Text('Result', readonly=True)
    error_message = fields.Text('Error', readonly=True)
    execution_time = fields.Float('Execution Time (s)', readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('xmlrpc.operation') or 'New'
        return super().create(vals)

    def action_execute(self):
        self.ensure_one()
        start_time = datetime.now()

        try:
            # Get connection
            conn = self.connection_id
            common = xmlrpc.client.ServerProxy(f'{conn.url}/xmlrpc/2/common')
            uid = common.authenticate(conn.database, conn.username, conn.password, {})

            if not uid:
                raise Exception('Authentication failed')

            models = xmlrpc.client.ServerProxy(f'{conn.url}/xmlrpc/2/object')

            # Execute based on operation type
            result = self._execute_operation(models, uid, conn)

            # Update record
            execution_time = (datetime.now() - start_time).total_seconds()
            self.write({
                'state': 'done',
                'result': str(result),
                'execution_time': execution_time,
                'error_message': False
            })

            # Log operation
            self.env['xmlrpc.log'].create({
                'handler_id': self.id,
                'execution_time': execution_time,
                'result': str(result)
            })

            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.write({
                'state': 'failed',
                'error_message': str(e),
                'execution_time': execution_time
            })
            _logger.error('XML-RPC Operation failed: %s', str(e))
            raise

    def _execute_operation(self, models, uid, conn):
        """Execute the XML-RPC operation"""
        if self.operation == 'search':
            domain = eval(self.domain or '[]')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'search',
                [domain]
            )

        elif self.operation == 'read':
            ids = eval(self.ids_list or '[]')
            fields = eval(self.fields_list or '[]')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'read',
                [ids], {'fields': fields}
            )

        elif self.operation == 'search_read':
            domain = eval(self.domain or '[]')
            fields = eval(self.fields_list or '[]')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'search_read',
                [domain], {'fields': fields}
            )

        elif self.operation == 'create':
            values = eval(self.values or '{}')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'create',
                [values]
            )

        elif self.operation == 'write':
            ids = eval(self.ids_list or '[]')
            values = eval(self.values or '{}')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'write',
                [ids, values]
            )

        elif self.operation == 'unlink':
            ids = eval(self.ids_list or '[]')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, 'unlink',
                [ids]
            )

        elif self.operation == 'execute':
            args = eval(self.method_args or '[]')
            kwargs = eval(self.method_kwargs or '{}')
            return models.execute_kw(
                conn.database, uid, conn.password,
                self.model_name, self.method_name,
                args, kwargs
            )