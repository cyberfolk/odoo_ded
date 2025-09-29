from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    def get_code(self):
        code = super().get_code()
        if self.type == "v1_19_q" and self.index:
            code = f"{self.quad_id.code}"
            code += f".{str(self.circle_order).zfill(2)}"
            code += f".{str(self.circle_number).zfill(2)}"
        return code
