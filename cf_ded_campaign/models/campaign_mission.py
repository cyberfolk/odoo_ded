from odoo import fields, models

MISSION_SATE_LIST = [('todo', 'Da fare'), ('ongoing', 'In corso'), ('done', 'Terminata')]


class CampaignMission(models.Model):
    _name = "campaign.mission"
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
        selection=MISSION_SATE_LIST,
        default="active",
        help="Stato della campagna",
    )
