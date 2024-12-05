from odoo import http
from odoo.http import request
import json
from datetime import datetime

class CustomAPIController(http.Controller):
    @http.route('/api/v1/sales_orders', auth='api_key', type='json', methods=['GET'])
    def get_sales_orders(self, **kwargs):
        try:
            sales_orders = request.env['sale.order'].search_read(
                domain=[],
                fields=['name', 'date_order', 'amount_total', 'partner_id', 'state']
            )
            return {'status': 'success', 'data': sales_orders}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/v1/chart_of_accounts', auth='api_key', type='json', methods=['GET'])
    def get_chart_of_accounts(self, **kwargs):
        try:
            accounts = request.env['account.account'].search_read(
                domain=[],
                fields=['code', 'name', 'account_type', 'internal_group']
            )
            return {'status': 'success', 'data': accounts}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}