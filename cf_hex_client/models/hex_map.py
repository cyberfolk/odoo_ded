import json
from itertools import groupby

from odoo import models, api, Command


class HexMap(models.Model):
    _inherit = "hex.map"

    def add_right(self):
        for row_i in range(self.row_min, self.row_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": row_i, "col": self.col_max + 1}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_map(self.id)

    def add_top(self):
        for col_i in range(self.col_min, self.col_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": self.row_min - 1, "col": col_i}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_map(self.id)

    def add_bottom(self):
        for col_i in range(self.col_min, self.col_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": self.row_max + 1, "col": col_i}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_map(self.id)

    def add_left(self):
        for row_i in range(self.row_min, self.row_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": row_i, "col": self.col_min - 1}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_map(self.id)

    @api.model
    def get_json_map_list(self):
        """Metodo richiamato dal orm di CurrentMap.js
            :return: Json della lista di tutte le Mappe nel DB."""
        map_fields = ['id', 'name']
        map_list = self.env['hex.map'].search([]).read(map_fields)
        json_map = json.dumps(map_list)
        return json_map

    @api.model
    def get_json_map(self, map_id):
        """Metodo richiamato dal orm di view_map.js
            :return: Json delle Mappe."""
        map_id = int(map_id)
        self_map = self.env['hex.map'].browse(map_id)
        quad_fields = ['id', 'code', 'index', 'row', 'col', 'hex_ids']
        hex_fields = ['id', 'code', 'index', 'row', 'col', 'color', 'hex_asset_id']

        # Otteniamo tutti i quad e i relativi hex in una singola query
        quads = self_map.quad_ids.read(quad_fields)
        hex_map = {quad['id']: self.env['hex.hex'].browse(quad['hex_ids']).read(hex_fields) for quad in quads}

        # Aggiungo le info relative a gli hex_asset negli hex
        hex_asset_fields = ['asset_id', 'rotation']
        hex_assets = self.env['hex.asset.tile'].search([]).read(hex_asset_fields)
        hex_assets_map = {x['id']: {'tile_id': x['asset_id'][0], 'rotation': x['rotation']} for x in hex_assets}
        for k, v in hex_map.items():
            for _hex in v:
                if _hex['hex_asset_id']:
                    _id = _hex['hex_asset_id'][0]
                    _hex['hex_asset_id'] = hex_assets_map[_id]

        dict_map = {
            'id': map_id,
            'type': self_map.type,
            'quad_ids': [{
                'id': quad['id'],
                'row': quad['row'],
                'code': quad['code'],
                'index': quad['index'],
                'col': quad['col'],
                'hex_ids': hex_map[quad['id']],
            } for quad in quads]
        }

        if self_map.type == 'v2_nolimit_q':
            quad_ids = dict_map.pop('quad_ids')
            quad_ids.sort(key=lambda x: (x["row"], x["col"]))
            quad_rows = [list(v) for k, v in groupby(quad_ids, key=lambda x: x['row'])]
            dict_map['quad_rows'] = quad_rows

        json_map = json.dumps(dict_map)
        return json_map
