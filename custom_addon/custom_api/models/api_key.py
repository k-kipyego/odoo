from odoo import models, fields, api
import secrets


class APIKey(models.Model):
    _name = 'custom.api.key'
    _description = 'API Key Management'

    name = fields.Char('Description', required=True)
    key = fields.Char('API Key', readonly=True)
    user_id = fields.Many2one('res.users', 'User', required=True)
    active = fields.Boolean('Active', default=True)
    last_used = fields.Datetime('Last Used')

    @api.model
    def create(self, vals):
        vals['key'] = secrets.token_urlsafe(32)
        return super(APIKey, self).create(vals)