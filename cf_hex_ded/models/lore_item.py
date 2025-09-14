from odoo import fields, models, api, Command


class LoreItem(models.Model):
    _inherit = "lore.item"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="lore_item_hex_rel",
        string="HEXs",
    )
