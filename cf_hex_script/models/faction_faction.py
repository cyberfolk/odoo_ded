from odoo import fields, models


class FactionFaction(models.Model):
    _inherit = "faction.faction"
    _description = "Fazione"

    npc_ids = fields.Many2many(
        comodel_name="creature.npc",
        relation="faction_faction_creature_npc_rel",
        string="NPCs",
        help="NPC appartenenti alla fazione",
    )

    hex_script_ids = fields.Many2many(
        comodel_name="hex.script",
        relation="faction_faction_hex_script_rel",
        string="Esagoni Scriptati",
        help="Esagoni Scriptati in cui è presente la fazione",
    )
