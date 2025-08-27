# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Ded Campaign",
    'icon': '/cf_ded_campaign/static/description/icon.png',
    'sequence': 4,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Modelli per la gestione delle Campagne",
    'description':
        """In questo modulo vengono introdotti i modelli per la gestione delle Campagne.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/campaign_pg.xml",
        "views/campaign_session.xml",
        "views/campaign_campaign.xml",
        "views/res_partner.xml",
    ],
    'assets': {
        'web.assets_backend': [
            '/cf_ded_campaign/static/src/css/style.css',
            '/cf_ded_campaign/static/src/FieldPxWidget/*',
        ],
        'web.assets_frontend': [
            '/cf_ded_campaign/static/src/css/style.css',
        ]
    },

    'depends': ['cf_ded_base', 'base'],
    'demo': [],
    'application': False,
    'installable': True,
}
