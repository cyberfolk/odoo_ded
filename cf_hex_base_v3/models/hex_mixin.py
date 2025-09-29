from odoo import api, fields, models
from ..utility.constant import MAP_TYPE_SELECTION


class HexMixin(models.AbstractModel):
    _inherit = 'hex.mixin'

    type = fields.Selection(
        selection_add=[('v3_no_q', 'V3 NO Q')],
        ondelete='set null'
    )
