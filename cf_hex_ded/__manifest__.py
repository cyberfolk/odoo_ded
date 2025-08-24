# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Ded",
    'icon': '/cf_hex_ded/static/description/icon.png',
    'sequence': 4,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce gli Hex-Script nella Hex Map",
    'description':
        """In questo modulo vengono introdotti gli Hex-Script, ovvero i modelli che descrivono la lore del singolo
         esagoni, e li collegano ai relativi biomi e alle creature che lo popolano.""",
    'license': 'AGPL-3',
    'data': [
        "views/hex_hex.xml",
        "views/biome_biome.xml",
        "views/encounter_encounter.xml",
        "views/creature_npc.xml",
        "views/creature_faction.xml",
        "views/menu_root.xml",
        "views/settlement_settlement.xml",
    ],
    'depends': ['cf_hex_base', 'cf_ded_base', 'cf_multiple_image'],
    'demo': [],
    'application': False,
    'installable': True,
    'assets': {
        'web.assets_backend': [],
    },
}
