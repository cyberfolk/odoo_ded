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
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.monster.legendary",
        relation="quest_monster_rel",
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.npc",
        relation="quest_npc_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="quest_faction_rel",
    )
    # endregion
