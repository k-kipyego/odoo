from odoo import models, fields, api
from odoo.exceptions import UserError
from ..tools.config import XMLRPCConfig
import xmlrpc.client
import logging

_logger = logging.getLogger(__name__)


class XMLRPCHandler(models.Model):
    _name = 'xmlrpc.handler'
    _description = 'XML-RPC Operation Handler'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
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

    def action_execute(self):
        """Executes the selected XML-RPC operation."""
        if not self.operation:
            raise UserError("Please specify an operation to execute.")
        try:
            # Establish connection
            config = XMLRPCConfig()  # Assumes XMLRPCConfig is properly defined
            common = xmlrpc.client.ServerProxy(f"{config.url}/xmlrpc/2/common")
            uid = common.authenticate(config.db, config.username, config.api_key, {})
            models = xmlrpc.client.ServerProxy(f"{config.url}/xmlrpc/2/object")

            # Handle different operations
            if self.operation == 'search':
                domain = eval(self.domain or '[]')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'search', [domain]))
            elif self.operation == 'read':
                ids = eval(self.ids_list or '[]')
                fields = eval(self.fields_list or '[]')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'read', [ids], {'fields': fields}))
            elif self.operation == 'search_read':
                domain = eval(self.domain or '[]')
                fields = eval(self.fields_list or '[]')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'search_read', [domain], {'fields': fields}))
            elif self.operation == 'create':
                values = eval(self.values or '{}')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'create', [values]))
            elif self.operation == 'write':
                ids = eval(self.ids_list or '[]')
                values = eval(self.values or '{}')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'write', [ids, values]))
            elif self.operation == 'unlink':
                ids = eval(self.ids_list or '[]')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, 'unlink', [ids]))
            elif self.operation == 'execute':
                args = eval(self.method_args or '[]')
                kwargs = eval(self.method_kwargs or '{}')
                self.result = str(models.execute_kw(
                    config.db, uid, config.api_key,
                    self.model_name, self.method_name, args, kwargs))
            else:
                raise UserError("Invalid operation specified.")
            self.state = 'done'
        except Exception as e:
            _logger.error("XML-RPC Error: %s", str(e))
            self.error_message = str(e)
            self.state = 'failed'
