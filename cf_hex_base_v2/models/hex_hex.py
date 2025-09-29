from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    row = fields.Integer(
        string="Riga",
    )

    col = fields.Integer(
        string="Colonna",
    )

    def get_code(self):
        code = super().get_code()
        if self.type == "v2_nolimit_q":
            quad_row = rec.quad_id.row * 4
            quad_col = rec.quad_id.col * 4
            _row = rec.format_int_v2(quad_row + rec.row)
            _col = rec.format_int_v2(quad_col + rec.col)
            code = f"{_row}{_col}"
        return code
