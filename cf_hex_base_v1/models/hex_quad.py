import json

from odoo import api, fields, models, Command
from ..utility.constant import BORDERS_MAP
from ..utility.constant import EXTERNAL_BORDERS_MAP
from ..utility.constant import HEX_MISSING_INDEX
from ..utility.constant import SPECULAR_BORDERS_MAP


class Quadrant(models.Model):
    _inherit = "hex.quad"

    hex_list = fields.Json(
        string="Hex list",
        help="Campo d'appoggio per la creazione di hex_ids."
    )

    missing_ids = fields.Many2many(
        comodel_name='hex.hex',
        relation='quad_hex_missing_rel',
        string="Missing IDs"
    )

    def get_code(self):
        code = super().get_code()
        if self.type == "v1_19_q" and self.index:
            code = (chr(ord('A') + self.index - 1))
        return code

    @api.model_create_multi
    def create(self, vals):
        quad = super(Quadrant, self).create(vals)
        quad.name = f"Quadrante {quad.code}"
        if quad.type == "v1_19_q":
            if quad.code == 'void' or not quad.hex_list:
                return quad
            for index in quad.hex_list:
                hex_vals = {'index': index, 'status': 'grid', 'type': 'v1_19_q'}
                quad.hex_ids = [Command.create(hex_vals)]
        return quad

    def unlink(self):
        for rec in self:
            for hex in rec.hex_ids:
                hex.unlink()
        return super(Quadrant, self).unlink()

    def set_hexs_borders(self):
        """Impostare i bordi degli Esagoni. Setta a void i bordi degli esagoni esterni."""
        hex_void = self.env.ref('cf_hex_base_v1.hex_hex_void')
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
