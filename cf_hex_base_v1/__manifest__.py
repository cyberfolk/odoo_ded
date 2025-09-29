# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Base V1",
    'icon': '/cf_hex_base_v1/static/description/icon.png',
    'sequence': 1,
    'version': '0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli hex di tipologia V1",
    'description':
        """In questa modulo vengono introdotti gli hex di tipologia V1.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/hex_hex.xml",
        "views/hex_quad.xml",
        "views/hex_map.xml",
        "views/menu_root.xml",
        "data/hex.xml",
    ],
    'depends': [
        'base',
        'web',
        'cf_o2m_expand_popup',
        'cf_m2m_tags_link'
        'cf_hex_base'
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_base_v1',
    'assets': {},
}
