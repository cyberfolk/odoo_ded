from odoo import fields, models

QUEST_SATE_LIST = [('todo', 'Da fare'), ('ongoing', 'In corso'), ('done', 'Terminata')]


class QuestQuest(models.Model):
    _name = "quest.quest"
    _description = "Missione"

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

    # region M2M Entità narrative
    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="quest_poi_rel",
        # column1="quest_id",
        # column2="poi_id",
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="quest_monster_rel",
        # column1="quest_id",
        # column2="monster_id",
        domain=[("is_legendary", "=", True)],
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="quest_npc_rel",
        # column1="quest_id",
        # column2="npc_id",
        domain=[("is_npc", "=", True)],
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        # column1="quest_id",
        # column2="faction_id",
        relation="quest_faction_rel",
    )
    # endregion
