from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    def get_code(self):
        code = super().get_code()
        if self.type == "v3_no_q":
            # TODO
            code = f"v3_no_q"
        return code
