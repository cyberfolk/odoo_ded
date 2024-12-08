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
