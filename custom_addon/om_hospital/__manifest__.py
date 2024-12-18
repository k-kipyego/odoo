{
    'name': 'Hospital Management System',
    'author': 'Datawhizzy',
    'license': 'LGPL-3',
    'depends': [
        'mail', 'product', 'account'
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/patient_views.xml",
        "data/sequence.xml",
        "views/appointment_views.xml",
        "views/appointment_line_views.xml",
        "views/patient_readonly_views.xml",
        "views/patient_tag_views.xml",
        "views/account_move_views.xml",
        "views/menu.xml",
    ]
}