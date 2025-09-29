from odoo import fields, models, api, Command
from ..utility.constant import BORDERS_MAP, QUAD_LIST_V1, INDEX_MAP_19Q_LIST


class HexMap(models.Model):
    _inherit = "hex.map"

    type = fields.Selection(
        selection_add=[('v2_nolimit_q', 'V2 NOLIMIT Q')],
        ondelete={'v2_nolimit_q': 'set null'}
    )

    row_min = fields.Integer(string="Row Min", compute="compute_quad_stats")
    row_max = fields.Integer(string="Row Max", compute="compute_quad_stats")
    row_num = fields.Integer(string="Row Num", compute="compute_quad_stats")
    col_min = fields.Integer(string="Col Min", compute="compute_quad_stats")
    col_max = fields.Integer(string="Col Max", compute="compute_quad_stats")
    col_num = fields.Integer(string="Col Num", compute="compute_quad_stats")

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
        if map.type == 'v2_nolimit_q':
            quad_vals = {"row": 0, "col": 0, "type": "v2_nolimit_q"}
            map.quad_ids = [Command.create(quad_vals)]

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
