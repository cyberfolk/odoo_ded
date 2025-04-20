# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Data",
    'icon': '/cf_ded_base/static/description/cyberfolk.png',
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
        'cf_hex_client',
        'cf_hex_biome',
        'cf_hex_lore',
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_data',
    'assets': {},
}
