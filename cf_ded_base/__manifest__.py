# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | D&D Base",
    'icon': '/cf_ded_base/static/description/icon.png',
    'sequence': 2,
    'version': '0.0.1',
    'category': 'D&D',
    'author': "cyberfolk",
    'summary': "Introduce gli elementi base di Dungeons & Dragons",
    'description':
        """In questo modulo vengono introdotti gli elementi base di Dungeons & Dragons.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/biome_biome.xml",
        "views/structure_structure.xml",
        "views/creature_creature.xml",
        "views/creature_type.xml",
        "views/creature_tag.xml",
        "views/creature_encounter.xml",
        "views/creature_encounter_line.xml",
        "views/point_of_interest.xml",
        "views/creature_faction.xml",
        "views/creature_faction_tag.xml",
        "views/encounter_encounter.xml",
        "views/lore_item.xml",
        # "views/creature_roster.xml",
        "views/settlement_settlement.xml",
        "views/quest_quest.xml",
        # "reports/creature_roster.xml",
        "reports/root_report.xml",
    ],
    'depends': ['base', 'web'],
    'demo': [],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            '/cf_ded_base/static/src/css/style.css',
        ],
        'web.assets_frontend': [
            '/cf_ded_base/static/src/css/style.css',
        ]
    },
}
