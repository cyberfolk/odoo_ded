import json

from odoo import api, fields, models, Command
from ..utility.constant import BORDERS_MAP
from ..utility.constant import EXTERNAL_BORDERS_MAP
from ..utility.constant import HEX_MISSING_INDEX
from ..utility.constant import MACRO_MAP_TYPE_SELECTION
from ..utility.constant import SPECULAR_BORDERS_MAP
from ..utility.constant import COLOR_HEX_LIST


class Quadrant(models.Model):
    _name = "hex.quad"
    _inherit = ['hex.mixin']
    _description = "Quadrant, contains Hexagons."
    _order = 'row,col'

    macro_id = fields.Many2one(
        comodel_name='hex.macro',
        string="Macro Area",
    )

    hex_list = fields.Json(
        string="Hex list",
        help="Campo d'appoggio per la creazione di hex_ids."
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='quad_id',
    )

    missing_ids = fields.Many2many(
        comodel_name='hex.hex',
        relation='quad_hex_missing_rel',
        string="Missing IDs"
    )

    hook_widget = fields.Char(
        string="hook_widget",
        help="Usato solamente per agganciare il widget del quadrante."
    )

    border_N = fields.Many2one(
        comodel_name='hex.quad',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.quad',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.quad',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.quad',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.quad',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.quad',
        string="NW",
        help="Confine Nord-Ovest"
    )

    type = fields.Selection(
        selection=MACRO_MAP_TYPE_SELECTION,
        string="Tipo",
        default="v1_19_q",
    )

    row = fields.Integer(
        string="Riga",
    )

    col = fields.Integer(
        string="Colonna",
    )

    @api.depends('index', 'row', 'col', 'type')
    def _compute_code(self):
        for rec in self:
            if rec.type == "v1_19_q" and rec.index:
                rec.code = (chr(ord('A') + rec.index - 1))
            elif rec.type == "v2_nolimit_q":
                _row = self.format_int_v2(rec.row)
                _col = self.format_int_v2(rec.col)
                rec.code = f"{_row}{_col}"
            else:
                rec.code = 'void'

    @api.model_create_multi
    def create(self, vals):
        quad = super(Quadrant, self).create(vals)
        quad.name = f"Quadrante {quad.code}"
        if quad.type == "v1_19_q":
            if quad.code == 'void' or not quad.hex_list:
                return quad
            for index in quad.hex_list:
                hex_vals = {'color': COLOR_HEX_LIST[quad.index - 1], 'index': index}
                quad.hex_ids = [Command.create(hex_vals)]
        elif quad.type == "v2_nolimit_q":
            for i in range(16):
                hex_vals = {
                    'color': COLOR_HEX_LIST[(quad.row * 4 + quad.col) % 19],
                    'type': "v2_nolimit_q",
                    'row': i // 4,
                    'col': i % 4
                }
                quad.hex_ids = [Command.create(hex_vals)]
        return quad

    def unlink(self):
        for rec in self:
            for hex in rec.hex_ids:
                hex.unlink()
        return super(Quadrant, self).unlink()

    def set_hexs_borders(self):
        """Impostare i bordi degli Esagoni. Setta a void i bordi degli esagoni esterni."""
        hex_void = self.env.ref('cf_hex_base.hex_hex_void')
        index_to_hex = {x.index: x for x in self.hex_ids}  # Crea un dizionario per mappare gli index agli esagoni
        for hex in self.hex_ids:
            borders = BORDERS_MAP[hex.index]
            hex.border_N = index_to_hex.get(borders[0]) or hex_void
            hex.border_NE = index_to_hex.get(borders[1]) or hex_void
            hex.border_SE = index_to_hex.get(borders[2]) or hex_void
            hex.border_S = index_to_hex.get(borders[3]) or hex_void
            hex.border_SW = index_to_hex.get(borders[4]) or hex_void
            hex.border_NW = index_to_hex.get(borders[5]) or hex_void

    def set_hexs_external_borders(self):
        """Impostare i bordi degli Esagoni esterni."""
        filtered_hex_ids = self.hex_ids.filtered(lambda r: r.index != 1)
        for hex in filtered_hex_ids:
            hex_external_borders = EXTERNAL_BORDERS_MAP[hex.index]
            for border_key, border_value in hex_external_borders.items():
                quad_border_field, hex_border_index = border_value
                quad_border = self[quad_border_field]
                hex_border = quad_border.hex_ids.filtered(lambda x: x.index == hex_border_index)
                if hex[border_key].code == 'void' and hex_border:
                    hex[border_key] = hex_border

    def set_missing_ids(self):
        """Popola il campo che contiene gli esagoni mancanti."""
        all_index = list(range(1, 20))
        missing_index_list = list(set(all_index) - set(self.hex_ids.mapped('index')))
        for missing_index in missing_index_list:
            border_quad, target_index, borders = HEX_MISSING_INDEX[missing_index]
            missing_hex = self[border_quad].hex_ids.filtered(lambda x: x.index == target_index)
            self.missing_ids = [(4, missing_hex.id)]

            for border_key, border_idex in borders.items():
                target_hex = self.hex_ids.filtered(lambda x: x.index == border_idex)
                missing_hex[border_key] = target_hex
                specular_borders_key = SPECULAR_BORDERS_MAP[border_key]
                target_hex[specular_borders_key] = missing_hex
