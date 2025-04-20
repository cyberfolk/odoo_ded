from odoo import fields, models


class FactionFaction(models.Model):
    _inherit = "creature.faction"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="creature_faction_hex_script_rel",
        string="Esagoni Scriptati",
        help="Esagoni in cui è presente la fazione",
    )
