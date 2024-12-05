# __manifest__.py
{
    'name': 'Universal CRUD Handler',
    'version': '17.0.1.0.0',
    'summary': 'Universal CRUD Operations Handler for Odoo Modules',
    'description': """
        This module provides a centralized system for handling CRUD operations
        across different Odoo modules with:
        - Universal API endpoints
        - Operation logging
        - Access control
        - Batch operations support
    """,
    'category': 'Technical',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',

    # Dependencies
    'depends': [
        'base',
        'web',
        'mail',
        'sale',  # Add modules you need to interact with
        'account',
        'stock',
    ],

    # Data files
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/crud_views.xml',
        'views/crud_log_views.xml',
        'views/crud_config_views.xml',
        'views/menu_items.xml',
        'data/crud_config_data.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'universal_crud/static/src/js/crud_widget.js',
            'universal_crud/static/src/css/crud_style.css',
        ],
    },

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}