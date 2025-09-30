from odoo import fields, models, api, Command


class HexMap(models.Model):
    _inherit = "hex.map"

    type = fields.Selection(
        selection_add=[('v2_nolimit_q', 'V2 NOLIMIT Q')],
        ondelete={'v2_nolimit_q': 'set null'}
    )

    @api.model_create_multi
    def create(self, vals_list):
        map = super().create(vals_list)
        if map.type == 'v2_nolimit_q':
            quad_vals = {"row": 0, "col": 0, "type": "v2_nolimit_q"}
            map.quad_ids = [Command.create(quad_vals)]

        return map

    def get_row_col(self):
        row_min, row_max, row_num, col_min, col_max, col_num = super().get_row_col()

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
