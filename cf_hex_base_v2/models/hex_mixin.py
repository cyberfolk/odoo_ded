from odoo import api, fields, models


class HexMixin(models.AbstractModel):
    _inherit = 'hex.mixin'

    type = fields.Selection(
        selection_add=[('v2_nolimit_q', 'V2 NOLIMIT Q')],
        ondelete={'v2_nolimit_q': 'set null'}
    )
