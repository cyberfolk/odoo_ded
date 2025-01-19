# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Campaign",
    'icon': '/cf_hex_base/static/description/cyberfolk.png',
    'sequence': 4,
    'version': '0.0.1',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "TODO",
    'description':
        """TODO.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/campaign_pg.xml",
        "views/campaign_session.xml",
        "views/campaign_campaign.xml",
        "views/res_partner.xml",
        "views/campaign_mission.xml",
    ],
    'assets': {
        'web.assets_backend': [
            '/cf_hex_campaign/static/src/css/style.css',
            '/cf_hex_campaign/static/src/FieldPxWidget/*',
        ],
        'web.assets_frontend': [
            '/cf_hex_campaign/static/src/css/style.css',
        ]
    },

    'post_init_hook': 'post_init_hook_cf_hex_campaign',
    'depends': ['cf_hex_biome', 'contacts'],
    'demo': [],
    'application': False,
    'installable': True,
}
