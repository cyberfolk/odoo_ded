from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    def get_code(self):
        code = super().get_code()
        if self.type == "v2_nolimit_q":
            quad_row = self.quad_id.row * 4
            quad_col = self.quad_id.col * 4
            _row = self.format_n_or_p(quad_row + self.row)
            _col = self.format_n_or_p(quad_col + self.col)
            code = f"{_row}{_col}"
        return code
