from odoo import models, fields

class APILog(models.Model):
    _name = 'custom.api.log'
    _description = 'API Request Logs'
    _order = 'create_date desc'

    name = fields.Char('Endpoint', required=True)
    method = fields.Char('HTTP Method', required=True)
    request_data = fields.Text('Request Data')
    response_data = fields.Text('Response Data')
    status_code = fields.Integer('Status Code')
    api_key_id = fields.Many2one('custom.api.key', 'API Key Used')
    ip_address = fields.Char('IP Address')