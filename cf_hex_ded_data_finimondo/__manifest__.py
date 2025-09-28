# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Data Finimondo",
    'icon': '/cf_hex_ded_data_finimondo/static/description/icon.png',
    'sequence': 3,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce i Biomi nella Hex Map",
    'description':
        """In questo modulo vengono salvati i dati per popolare i record.""",
    'license': 'AGPL-3',
    'data': [],
    'depends': [
        'cf_hex_ded_data_base',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init__cf_hex_ded_data_finimondo',
    'assets': {},
}
