from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    def get_code(self):
        code = super().get_code()
        if self.type == "v3_no_q":
            _row = self.format_int_v2(self.row)
            _col = self.format_int_v2(self.col)
            code = f"{_row}{_col}"
        return code
