from odoo import api, fields, models


class HexMixin(models.AbstractModel):
    _inherit = 'hex.mixin'

    type = fields.Selection(
        selection_add=[('v1_19_q', 'V1 19 Q')],
        ondelete='set null'
    )

    circle_order = fields.Integer(
        string='Circle Order',
        compute='_compute_circle_order',
    )

    circle_number = fields.Integer(
        string='Circle Number',
        compute='_compute_circle_number',
    )

    @api.depends('index')
    def _compute_circle_order(self):
        for record in self:
            if record.index == 1:
                record.circle_order = 0
            elif 2 <= record.index <= 7:
                record.circle_order = 1
            elif 8 <= record.index <= 19:
                record.circle_order = 2
            else:
                record.circle_order = None

    @api.depends('index')
    def _compute_circle_number(self):
        for record in self:
            if record.index == 1:
                record.circle_number = 1
            elif 2 <= record.index <= 7:
                record.circle_number = record.index - 1
            elif 8 <= record.index <= 19:
                record.circle_number = record.index - 7
            else:
                record.circle_number = None

    # Ideati per altri Hex, Quad e Map con le Form View
    # Ma avendole bloccate -> valutare di togliere questi metodi
    @api.constrains('index')
    def _check_index(self):
        for record in self:
            if record.index < 0 or record.index > 19:
                raise ValidationError("Il valore di 'index' deve essere compreso tra 1 e 19.")

    @staticmethod
    def format_int_v2(num):
        """Ritorna 'N<|num|>' o 'P<|num|>' in base al segno di num"""
        prefix = "N" if num < 0 else "P"
        return f"{prefix}{abs(num)}"
