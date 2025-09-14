from odoo import fields, models


class Settlement(models.Model):
    _inherit = "quest.quest"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="quest_hex_rel",
        string="HEXs",
    )
