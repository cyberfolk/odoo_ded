# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    "name": "Cyberfolk | D&D Narrative Relation",
    'icon': '/cf_ded_narrative_relation/static/description/icon.png',
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
        "mail"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/narrative_relation_views.xml",
        "views/narrative_relation_buttons.xml",
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'assets': {},
}
