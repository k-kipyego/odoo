# __manifest__.py
{
    'name': 'Odoo XML-RPC Handler',
    'version': '17.0.1.0.0',
    'summary': 'Handle XML-RPC Operations Across Odoo Modules',
    'description': """
        XML-RPC Handler for Odoo Operations:
        - Supports all CRUD operations
        - Built-in logging and monitoring
        - Batch operation support
        - Connection management
    """,
    'category': 'Technical',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/xmlrpc_views.xml',
        'views/menu_items.xml',
        'wizard/xmlrpc_operations_wizard_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}