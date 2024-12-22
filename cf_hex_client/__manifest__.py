# -*- coding: utf-8 -*-
# Powered by cyberfolk

{
    'name': "Cyberfolk | Hex Client",
    'icon': '/cf_hex_client/static/description/cyberfolk.png',
    'sequence': 1,
    'version': '17.0',
    'category': 'Map',
    'author': "cyberfolk",
    'summary': "Introduce un interfaccia più semplice per le mappe.",
    'description':
        """In questo modulo viene introdotto un menù che mette a disposizione un'interfaccia per poter
        interagire direttamente con le mappe in modo più semplice.""",
    'license': 'AGPL-3',
    'data': [
        "security/ir.model.access.csv",
        "views/menu_root.xml",
        "views/asset_tile.xml",
        "views/hex_quad.xml",
    ],
    'depends': [
        'base',
        'web',
        'cf_o2m_expand_popup',
        'cf_m2m_tags_link',
        'cf_hex_lore'
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'assets': {
        'web.assets_backend': [
            '/cf_hex_client/static/src/utility/utils.js',
            '/cf_hex_client/static/src/store.js',
            '/cf_hex_client/static/src/scss/style.scss',
            '/cf_hex_client/static/src/QuadWidget/*',
            '/cf_hex_client/static/src/ViewMapClient/ViewMapClient.js',
            '/cf_hex_client/static/src/ViewMapClient/ViewMapClient.xml',
            '/cf_hex_client/static/src/ViewMapClient/AddQuadrant/*',
            '/cf_hex_client/static/src/ViewMapClient/HideShow/*',
            '/cf_hex_client/static/src/ViewMapClient/ViewMap/*',
            '/cf_hex_client/static/src/ViewMapClient/CurrentBiome/*',
            '/cf_hex_client/static/src/ViewMapClient/CurrentZoom/*',
            '/cf_hex_client/static/src/ViewMapClient/CurrentTiles/*',
            '/cf_hex_client/static/src/ViewMapClient/CurrentMap/*',
            '/cf_hex_client/static/src/ViewMapClient/ClearCurrent/*',
            '/cf_hex_client/static/src/ViewMapClient/DirTiles/*',
            '/cf_hex_client/static/src/ViewMapClient/HexHex/*',
        ],
        'web.assets_frontend': [
            '/cf_hex_client/static/src/scss/style.scss',
        ]
    },
}
