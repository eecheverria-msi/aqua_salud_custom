# -*- coding: utf-8 -*-
{
    'name': "Aqua Salud Custom",

    'summary': """
        Aqua Salud Custom""",

    'description': """
        Aqua Salud Custom
    """,

    'author': "Integer.ie",
    'website': "https://integer.ie",
    'category': 'Productivity',
    'version': '17.0.1.0',
    'images': [
        'static/description/icon.png',
    ],
    'depends': [
        'web',
        'base',
        'mail',
        'contacts',
        'base_setup',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/Anamnesis/anamnesis.xml',
        'views/Other/res_partner.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}