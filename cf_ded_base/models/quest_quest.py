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
