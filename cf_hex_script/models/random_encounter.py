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

    hex_script_id = fields.Many2one(
        comodel_name="hex.script",
        string="Hex Script",
    )

    # todo aggiungere npc
