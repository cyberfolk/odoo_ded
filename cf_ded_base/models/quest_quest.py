from odoo import fields, models
from ..utility.selection import QUEST_SATE_LIST


class QuestQuest(models.Model):
    _name = "quest.quest"
    _inherit = "mixin.narrative.entity"
    _description = "Missione"

    _sql_constraints = [
        ("unique_artifact_artifact_name", "UNIQUE(name)", "Il nome della Missione deve essere univoco!"),
    ]

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    state = fields.Selection(
        string="Stato",
        selection=QUEST_SATE_LIST,
        default="ongoing",
        help="Stato della campagna",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - DESCRIPTIVE ----------------------------------------------------------------------------------
    hook = fields.Text(
        string="Hook",
        help="Il gancio, il motivo per cui i PG si interessano (curiosità, sopravvivenza, dovere, ricompensa).",
    )
    objective = fields.Text(
        string="Obiettivo",
        help="Cosa bisogna fare, in termini chiari e raggiungibili.",
    )
    key_steps = fields.Text(
        string="Passaggi chiave",
        help="Micro-task o dettagli operativi che chiariscono meglio l’obiettivo.",
    )
    rewards = fields.Text(
        string="Ricompense",
        help="Ciò che si ottiene se la quest viene completata (oro, prestigio, conoscenze, alleanze).",
    )
    risks = fields.Text(
        string="Rischi",
        help="Ciò che si rischia se la quest viene fallita o ignorata (perdita, morte, maledizione, rovina sociale).",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    settlement_ids = fields.Many2many(
        string="Insediamenti",
        comodel_name="settlement.settlement",
        relation="settlement_quest_rel",
    )
    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="quest_poi_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="quest_faction_rel",
    )
    lore_item_ids = fields.Many2many(
        string="Lore Items",
        comodel_name="lore.item",
        relation="quest_lore_item_rel",
    )
    artifact_ids = fields.Many2many(
        string="Artefatti",
        comodel_name="artifact.artifact",
        relation="artifact_quest_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="quest_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="quest_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="quest_monster_rel",
        domain=[('is_legendary', '=', True)]
    )
    # endregion --------------------------------------------------------------------------------------------------------
