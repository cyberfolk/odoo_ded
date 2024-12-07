import json
from itertools import groupby

from odoo import fields, models, api, Command
from ..utility.constant import BORDERS_MAP
from ..utility.constant import MACRO_MAP_TYPE_SELECTION
from ..utility.constant import QUAD_LIST_V1


class MacroArea(models.Model):
    _name = "hex.macro"
    _description = "Macro-Area, contains Quadrants."

    name = fields.Char(
        string='Name',
    )

    quad_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='macro_id',
    )

    type = fields.Selection(
        selection=MACRO_MAP_TYPE_SELECTION,
        string="Tipo",
        default="v1_19_q",
    )

    row_min = fields.Integer(string="Row Min", compute="compute_quad_stats")
    row_max = fields.Integer(string="Row Max", compute="compute_quad_stats")
    row_num = fields.Integer(string="Row Num", compute="compute_quad_stats")
    col_min = fields.Integer(string="Col Min", compute="compute_quad_stats")
    col_max = fields.Integer(string="Col Max", compute="compute_quad_stats")
    col_num = fields.Integer(string="Col Num", compute="compute_quad_stats")

    def set_quads_borders(self):
        """Impostare i bordi dei quadranti. Dal secondo cerchio in poi ci potrebbero essere bordi che non
        confinano con nulla, in quel caso quei bordi verranno settati a void."""
        quad_void = self.env.ref('cf_hex_base.hex_quad_void')
        index_to_quad = {x.index: x for x in self.quad_ids}  # Crea un dizionario per mappare gli index agli esagoni
        for quad in self.quad_ids:
            borders = BORDERS_MAP[quad.index]
            quad.border_N = index_to_quad.get(borders[0]) or quad_void
            quad.border_NE = index_to_quad.get(borders[1]) or quad_void
            quad.border_SE = index_to_quad.get(borders[2]) or quad_void
            quad.border_S = index_to_quad.get(borders[3]) or quad_void
            quad.border_SW = index_to_quad.get(borders[4]) or quad_void
            quad.border_NW = index_to_quad.get(borders[5]) or quad_void

    @api.model_create_multi
    def create(self, vals_list):
        """Serve per settare:
            - La lista dei Quadranti e relative liste degli Esagoni,
            - I confini dei Quadranti,
            - I confini interni degli Esagoni
            - I confini esterni degli Esagoni
            - La lista degli Esagoni mancanti
        """
        macro = super().create(vals_list)
        if macro.type == 'v2_nolimit_q':
            quad_vals = {"row": 0, "col": 0, "type": "v2_nolimit_q"}
            macro.quad_ids = [Command.create(quad_vals)]

        elif macro.type == 'v1_19_q':
            for quad_vals in QUAD_LIST_V1:
                quad_vals['type'] = 'v1_19_q'
                macro.quad_ids = [Command.create(quad_vals)]

            macro.set_quads_borders()
            for quad in macro.quad_ids:
                quad.set_hexs_borders()
            for quad in macro.quad_ids:
                quad.set_hexs_external_borders()
            for quad in macro.quad_ids:
                quad.set_missing_ids()
        return macro

    def unlink(self):
        for rec in self:
            for quad in rec.quad_ids:
                quad.unlink()
        return super(MacroArea, self).unlink()


    def compute_quad_stats(self):
        for rec in self:
            if not self.quad_ids:
                rec.row_min = None
                rec.row_max = None
                rec.row_num = None
                rec.col_min = None
                rec.col_max = None
                rec.col_num = None
            else:
                col_set = {x.col for x in self.quad_ids}
                row_set = {x.row for x in self.quad_ids}
                rec.row_min = min(row_set)
                rec.row_max = max(row_set)
                rec.row_num = rec.row_max - rec.row_min + 1
                rec.col_min = min(col_set)
                rec.col_max = max(col_set)
                rec.col_num = rec.col_max - rec.col_min + 1

    def add_right(self):
        for row_i in range(self.row_min, self.row_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": row_i, "col": self.col_max + 1}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_macro(self.id)

    def add_top(self):
        for col_i in range(self.col_min, self.col_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": self.row_min - 1, "col": col_i}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_macro(self.id)

    def add_bottom(self):
        for col_i in range(self.col_min, self.col_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": self.row_max + 1, "col": col_i}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_macro(self.id)

    def add_left(self):
        for row_i in range(self.row_min, self.row_max + 1):
            quad_vals = {"type": "v2_nolimit_q", "row": row_i, "col": self.col_min - 1}
            self.quad_ids = [Command.create(quad_vals)]
        return self.get_json_macro(self.id)

    # region METODI CHIAMATI DAJAVASCRIPT ------------------------------------------------------------------------------
    @api.model
    def get_json_map_list(self):
        """Metodo richiamato dal orm di CurrentMap.js
            :return: Json della lista di tutte le Macro-Aree nel DB."""
        map_fields = ['id', 'name']
        map_list = self.env['hex.macro'].search([]).read(map_fields)
        json_map = json.dumps(map_list)
        return json_map

    @api.model
    def get_json_macro(self, macro_id):
        """Metodo richiamato dal orm di view_macro.js
            :return: Json della Macro-Area."""
        macro_id = int(macro_id)
        self_macro = self.env['hex.macro'].browse(macro_id)
        quad_fields = ['id', 'code', 'index', 'row', 'col', 'hex_ids']
        hex_fields = ['id', 'code', 'index', 'row', 'col', 'color', 'hex_asset_id']

        # Otteniamo tutti i quad e i relativi hex in una singola query
        quads = self_macro.quad_ids.read(quad_fields)
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

        dict_macro = {
            'id': macro_id,
            'type': self_macro.type,
            'quad_ids': [{
                'id': quad['id'],
                'row': quad['row'],
                'code': quad['code'],
                'index': quad['index'],
                'col': quad['col'],
                'hex_ids': hex_map[quad['id']],
            } for quad in quads]
        }

        if self_macro.type == 'v2_nolimit_q':
            quad_ids = dict_macro.pop('quad_ids')
            quad_ids.sort(key=lambda x: (x["row"], x["col"]))
            quad_rows = [list(v) for k, v in groupby(quad_ids, key=lambda x: x['row'])]
            dict_macro['quad_rows'] = quad_rows

        json_macro = json.dumps(dict_macro)
        return json_macro
    # endregion --------------------------------------------------------------------------------------------------------
