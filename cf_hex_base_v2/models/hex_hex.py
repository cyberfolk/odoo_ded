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
            quad_row = self.quad_id.row * 4
            quad_col = self.quad_id.col * 4
            _row = self.format_int_v2(quad_row + self.row)
            _col = self.format_int_v2(quad_col + self.col)
            code = f"{_row}{_col}"
        return code
