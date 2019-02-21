{
    'name': 'School Management 2.0',
    'summary': """School Management by Danimar""",
    'version': '11.0.1.0.0',
    'author': 'Trustcode',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/class.xml',
        'views/enrollment.xml',
        'views/menus.xml',
        'views/res_partner.xml',
        'report/enrollment.xml',
        'report/enrollment_templates.xml',
        'views/website_templates.xml',
    ],
    'application': True,
}
