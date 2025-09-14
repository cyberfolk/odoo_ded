from odoo import fields, models


class Settlement(models.Model):
    _inherit = "settlement.settlement"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="settlement_hex_rel",
        string="HEXs",
    )
