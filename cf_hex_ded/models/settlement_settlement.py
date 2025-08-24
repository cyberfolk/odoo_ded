from odoo import fields, models


class Settlement(models.Model):
    _inherit = "settlement.settlement"

    hex_ids = fields.One2many(
        "hex.hex",
        "settlement_id",
        string="Esagoni"
    )
