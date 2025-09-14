from odoo import fields, models


class ArtifactArtifact(models.Model):
    _name = "artifact.artifact"
    _inherit = "mixin.narrative.entity"
    _description = "Artefatto"

    _sql_constraints = [
        ("unique_artifact_artifact_name", "UNIQUE(name)", "Il nome dell'Artefatto deve essere univoco!"),
    ]

    # region FIELDS - DESCRIPTIVE ----------------------------------------------------------------------------------
    # ...
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    settlement_ids = fields.Many2many(
        string="Insediamenti",
        comodel_name="settlement.settlement",
        relation="settlement_artifact_rel",
    )
    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="artifact_poi_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="artifact_faction_rel",
    )
    lore_item_ids = fields.Many2many(
        string="Lore Items",
        comodel_name="lore.item",
        relation="artifact_lore_item_rel",
    )
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="artifact_quest_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="artifact_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="artifact_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="artifact_monster_rel",
        domain=[('is_legendary', '=', True)]
    )
    # endregion --------------------------------------------------------------------------------------------------------
