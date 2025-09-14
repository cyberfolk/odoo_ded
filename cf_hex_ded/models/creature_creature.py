from odoo import fields, models, api, Command


class CreatureCreature(models.Model):
    _inherit = "creature.creature"

    hex_ids = fields.Many2many(
        string="(Base) HEXs",
        comodel_name="hex.hex",
        relation="hex_creature_rel",
    )
    hex_npc_ids = fields.Many2many(
        string="(NPC) HEXs",
        comodel_name="hex.hex",
        relation="hex_npc_rel",
    )
    hex_monster_ids = fields.Many2many(
        string="(Monster) HEXs",
        comodel_name="hex.hex",
        relation="hex_monster_rel",
    )
