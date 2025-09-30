from odoo import api, fields, models, Command


class Quadrant(models.Model):
    _inherit = "hex.quad"
    _order = 'row,col'

    def get_code(self):
        code = super().get_code()
        if self.type == "v2_nolimit_q":
            _row = self.format_n_or_p(self.row)
            _col = self.format_n_or_p(self.col)
            code = f"{_row}{_col}"
        return code

    @api.depends('index', 'row', 'col', 'type')
    def _compute_code(self):
        for rec in self:
            code = rec.get_code()
            rec.code = code

    @api.model_create_multi
    def create(self, vals):
        quad = super(Quadrant, self).create(vals)
        quad.name = f"Quadrante {quad.code}"
        if quad.type == "v2_nolimit_q":
            for i in range(16):
                hex_vals = {
                    'map_id': quad.map_id.id,
                    'type': "v2_nolimit_q",
                    'status': 'grid',
                    'row': i // 4,
                    'col': i % 4
                }
                quad.hex_ids = [Command.create(hex_vals)]
        return quad
