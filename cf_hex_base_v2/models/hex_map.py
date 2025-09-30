from odoo import fields, models, api, Command


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
            row_min, row_max, row_num, col_min, col_max, col_num = rec.get_quad_stats()
            rec.row_min = row_min
            rec.row_max = row_max
            rec.row_num = row_num
            rec.col_min = col_min
            rec.col_max = col_max
            rec.col_num = col_num

    def get_quad_stats(self):
        self.ensure_one()
        row_min = row_max = row_num = None
        col_min = col_max = col_num = None

        # condizione opzionale sul tipo
        if self.type == "v2_nolimit_q" and self.quad_ids:
            row_set = {quad.row for quad in self.quad_ids}
            col_set = {quad.col for quad in self.quad_ids}

            row_min = min(row_set)
            row_max = max(row_set)
            row_num = row_max - row_min + 1
            col_min = min(col_set)
            col_max = max(col_set)
            col_num = col_max - col_min + 1

        return row_min, row_max, row_num, col_min, col_max, col_num
