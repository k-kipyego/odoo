{
    'name': 'Custom API Integration',
    'version': '1.0',
    'category': 'Technical',
    'summary': 'Custom API endpoints for Odoo integration',
    'description': """
        This module provides custom API endpoints for:
        - Sales Orders
        - Chart of Accounts
        - API Key Management
        - Request Logging
    """,
    'author': 'datawhizyy',
    'website': 'your-website.com',
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/api_views.xml',
        'views/api_menu.xml',
        'data/api_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}