# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Base V3",
    'icon': '/cf_hex_base_v3/static/description/icon.png',
    'sequence': 1,
    'version': '0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli hex di tipologia V3",
    'description':
        """In questa modulo vengono introdotti gli hex di tipologia V3.""",
    'license': 'AGPL-3',
    'data': [
        "views/hex_hex.xml",
        "views/hex_quad.xml",
        "views/hex_map.xml",
    ],
    'depends': [
        'cf_hex_base'
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_base_v3',
    'assets': {},
}
