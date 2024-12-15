from odoo import fields, models, api


class RandomEncounter(models.Model):
    _name = "random.encounter"
    _description = "Random Encounter"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Hex-Script"
    )

    description = fields.Html(
        string="Descrizione",
    )

    # todo aggiungere npc
