from odoo import fields, models, api, Command


class HexMap(models.Model):
    _inherit = "hex.map"

    type = fields.Selection(
        selection_add=[('v3_no_q', 'V3 NO Q')],
        ondelete={'v3_no_q': 'set null'}
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='map_id',
    )

    @api.model_create_multi
    def create(self, vals_list):
        map = super().create(vals_list)
        if map.type == 'v3_no_q':
            hex_vals = {"row": 0, "col": 0, "type": "v3_no_q", "map_id": map.id}
            map.hex_ids = [Command.create(hex_vals)]

        return map

    def get_quad_stats(self):
        self.ensure_one()
        row_min = row_max = row_num = None
        col_min = col_max = col_num = None

        # condizione opzionale sul tipo
        if self.type == "v3_no_q" and self.hex_ids:
            row_set = self.hex_ids.mapped('row')
            col_set =self.hex_ids.mapped('col')

            row_min = min(row_set)
            row_max = max(row_set)
            row_num = row_max - row_min + 1
            col_min = min(col_set)
            col_max = max(col_set)
            col_num = col_max - col_min + 1

        return row_min, row_max, row_num, col_min, col_max, col_num
