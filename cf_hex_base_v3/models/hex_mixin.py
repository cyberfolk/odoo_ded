from odoo import api, fields, models


class HexMixin(models.AbstractModel):
    _inherit = 'hex.mixin'

    type = fields.Selection(
        selection_add=[('v3_no_q', 'V2 NO Q')],
        ondelete={'v2_no_q': 'set null'}
    )
