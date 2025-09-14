from odoo import fields, models


class FactionFaction(models.Model):
    _inherit = "creature.faction"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="faction_hex_rel",
        string="HEXs",
    )
