from odoo import fields, models

QUEST_SATE_LIST = [('todo', 'Da fare'), ('ongoing', 'In corso'), ('done', 'Terminata')]


class QuestQuest(models.Model):
    _name = "quest.quest"
    _description = "Missione"

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Campagna",
    )

    image = fields.Image(
        string="Immagine",
    )

    state = fields.Selection(
        string="Stato",
        selection=QUEST_SATE_LIST,
        default="ongoing",
        help="Stato della campagna",
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
