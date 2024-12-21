# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Base",
    'icon': '/cf_hex_base/static/description/icon.png',
    'sequence': 1,
    'version': '17.0',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli elementi base della Hex Map",
    'description':
        """In questa app vengono introdotti gli elementi base della Hex Map: ovvero Mappe, Quadranti ed Esagoni.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/hex_hex.xml",
        "views/hex_quad.xml",
        "views/hex_map.xml",
        "views/filter_apps.xml",
        "views/menu_root.xml",
        "data/hex.xml",
    ],
    'depends': [
        'base',
        'web',
        'cf_o2m_expand_popup',
        'cf_m2m_tags_link'
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'post_init_hook': 'post_init_hook_cf_hex_base',
    'assets': {},
}
