from odoo import fields, models, api, Command
from ..utility.constant import BORDERS_MAP, MAP_TYPE_SELECTION, QUAD_LIST_V1, INDEX_MAP_19Q_LIST


class HexMap(models.Model):
    _name = "hex.map"
    _description = "Mappa, contains Quadrants."

    type = fields.Selection(
        selection=MAP_TYPE_SELECTION,
        string="Tipo",
        default="v1_19_q",
        required=True,
    )

    # endregion --------------------------------------------------------------------------------------------------------

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

    def compute_quad_stats(self):
        for rec in self:
            if not rec.quad_ids:  # Caso in cui non ci sono quad_ids
                rec.row_min = rec.row_max = rec.row_num = None
                rec.col_min = rec.col_max = rec.col_num = None
                continue

            # Calcolo dei set di righe e colonne
            row_set = {quad.row for quad in rec.quad_ids}
            col_set = {quad.col for quad in rec.quad_ids}

            # Calcolo delle statistiche
            rec.row_min = min(row_set)
            rec.row_max = max(row_set)
            rec.row_num = rec.row_max - rec.row_min + 1
            rec.col_min = min(col_set)
            rec.col_max = max(col_set)
            rec.col_num = rec.col_max - rec.col_min + 1
