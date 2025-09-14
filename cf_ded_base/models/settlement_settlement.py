from odoo import fields, models
from ..utility.selection import SETTLEMENT_SCALE_LIST, ATTITUDE_LIST


class Settlement(models.Model):
    """
    Documentazione completa:
        https://cyberfolk.github.io/wm-docs/md/lore-tool/l02-insediamenti/
    """

    _name = "settlement.settlement"
    _inherit = "mixin.narrative.entity"
    _description = "Insediamento"

    _sql_constraints = [("unique_name", "UNIQUE(name)", "Il nome dell'Insediamento deve essere univoco!")]

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    scale = fields.Selection(
        selection=SETTLEMENT_SCALE_LIST,
        string="Scala",
        required=True,
        default="borgo",
    )
    attitude = fields.Selection(
        selection=ATTITUDE_LIST,
        string="Atteggiamento",
        required=True,
        default="neutrale",
    )
    needs = fields.Text(
        string="Bisogni"
    )
    offers = fields.Text(
        string="Offre"
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="settlement_quest_rel",
    )
    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="settlement_poi_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="settlement_faction_rel",
    )
    lore_item_ids = fields.Many2many(
        string="Lore Items",
        comodel_name="lore.item",
        relation="settlement_lore_item_rel",
    )
    artifact_ids = fields.Many2many(
        string="Artefatti",
        comodel_name="artifact.artifact",
        relation="settlement_artifact_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="settlement_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="settlement_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="settlement_monster_rel",
        domain=[('is_legendary', '=', True)]
    )
    # endregion --------------------------------------------------------------------------------------------------------
