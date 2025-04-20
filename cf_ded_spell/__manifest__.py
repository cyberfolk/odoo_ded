# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | D&D | Spell",
    'icon': '/cf_ded_spell/static/description/icon.png',
    'sequence': 2,
    'version': '0.0.1',
    'category': 'D&D',
    'author': "cyberfolk",
    'summary': "Introduce gli Incantesimi",
    'description':
        """In questo modulo vengono introdotti gli Incantesimi.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/spell.xml",
        "views/spell_list.xml",
        'reports/root_report.xml',
        'reports/spell_list.xml',
    ],
    'depends': [
        'cf_ded_base'
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'assets': {},
}
