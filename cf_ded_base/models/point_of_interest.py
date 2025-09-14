from odoo import fields, models, api


class PointOfInterest(models.Model):
    _name = "point.of.interest"
    _inherit = "mixin.narrative.entity"
    _description = "Punto d'Interesse"

    _sql_constraints = [("unique_name", "UNIQUE(name)", "Il nome del Punto d'Interesse deve essere univoco!")]

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="quest_poi_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazione",
        comodel_name="creature.faction",
        relation="poi_faction_rel",
    )
    settlement_ids = fields.Many2many(
        string="Insediamenti",
        comodel_name="settlement.settlement",
        relation="settlement_poi_rel",
    )
    lore_item_ids = fields.Many2many(
        string="Lore Items",
        comodel_name="lore.item",
        relation="poi_lore_item_rel",
    )
    artifact_ids = fields.Many2many(
        string="Artefatti",
        comodel_name="artifact.artifact",
        relation="artifact_poi_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="poi_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="poi_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="poi_monster_rel",
        domain=[('is_legendary', '=', True)]
    )
    # endregion --------------------------------------------------------------------------------------------------------
