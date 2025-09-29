from odoo import fields, models, api, Command
from ..utility.constant import BORDERS_MAP, QUAD_LIST_V1


class HexMap(models.Model):
    _inherit = "hex.map"

    type = fields.Selection(
        selection_add=[('v1_19_q', 'V1 19 Q')],
        ondelete={'v1_19_q': 'set null'}
    )

    def set_quads_borders(self):
        """Impostare i bordi dei quadranti. Dal secondo cerchio in poi ci potrebbero essere bordi che non
        confinano con nulla, in quel caso quei bordi verranno settati a void."""
        quad_void = self.env.ref('cf_hex_base_v1.hex_quad_void')
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
        map = super().create(vals_list)
        if map.type == 'v1_19_q':
            for quad_vals in QUAD_LIST_V1:
                quad_vals['type'] = 'v1_19_q'
                map.quad_ids = [Command.create(quad_vals)]

            map.set_quads_borders()
            for quad in map.quad_ids:
                quad.set_hexs_borders()
            for quad in map.quad_ids:
                quad.set_hexs_external_borders()
            for quad in map.quad_ids:
                quad.set_missing_ids()
        return map
