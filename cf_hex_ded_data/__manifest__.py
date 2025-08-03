# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Data",
    'icon': '/cf_hex_ded_data/static/description/icon.png',
    'sequence': 3,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce i Biomi nella Hex Map",
    'description':
        """In questo modulo vengono salvati i dati per popolare i record.""",
    'license': 'AGPL-3',
    'data': [
        "views/base.xml",
        "data/demo.xml",
    ],
    'depends': [
        'cf_ded_base',
        'cf_hex_base',
        'cf_hex_ded',
        'cf_hex_ded_client',
        'cf_data_handler',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init__cf_hex_ded_data',
    'assets': {},
}
