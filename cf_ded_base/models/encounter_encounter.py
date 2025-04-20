from odoo import fields, models, api


class RandomEncounter(models.Model):
    _name = "encounter.encounter"
    _description = "Random Encounter"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome dell'Incontro"
    )

    description = fields.Html(
        string="Descrizione",
    )

    # todo aggiungere npc
