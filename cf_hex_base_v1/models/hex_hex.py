from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"

    def get_code(self):
        code = super().get_code()
        if rec.type == "v1_19_q" and rec.index:
            code = f"{rec.quad_id.code}"
            code += f".{str(rec.circle_order).zfill(2)}"
            code += f".{str(rec.circle_number).zfill(2)}"
        return code
