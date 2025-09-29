from odoo import api, fields, models
from ..utility.constant import MAP_TYPE_SELECTION


class HexMixin(models.AbstractModel):
    _inherit = 'hex.mixin'

    type = fields.Selection(
        selection_add=[('v2_nolimit_q', 'V3 NOLIMIT Q')],
        ondelete='set null'
    )

    @staticmethod
    def format_int_v2(num):
        """Ritorna 'N<|num|>' o 'P<|num|>' in base al segno di num"""
        prefix = "N" if num < 0 else "P"
        return f"{prefix}{abs(num)}"
