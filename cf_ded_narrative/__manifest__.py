# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    "name": "Cyberfolk | D&D Narrative",
    'icon': '/cf_ded_narrative/static/description/icon.png',
    'sequence': 5,
    'version': '0.0.1',
    'category': 'D&D',
    'author': "cyberfolk",
    'summary': "Introduce le relazioni narrative",
    'description':
        """In questo modulo vengono introdotte le relazioni narrative tra record.""",
    "license": "AGPL-3",
    "depends": [
        "base",
        "cf_ded_base",
        "cf_ded_campaign"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/narrative_relation.xml",
        "views/creature_npc.xml",
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'assets': {},
}
