from odoo import fields, models


class FactionFaction(models.Model):
    _inherit = "creature.faction"
    _description = "Fazione"

    hex_script_ids = fields.Many2many(
        comodel_name="hex.script",
        relation="creature_faction_hex_script_rel",
        string="Esagoni Scriptati",
        help="Esagoni Scriptati in cui è presente la fazione",
    )
