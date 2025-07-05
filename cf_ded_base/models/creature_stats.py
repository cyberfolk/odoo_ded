from odoo import fields, models


class CreatureCreature(models.AbstractModel):
    _name = "creature.stats"
    _description = "Creature Caratteristiche Comuni"

    name = fields.Char(
        string="Nome",
        required=True,
    )

    _sql_constraints = [
        ('unique_creature_stats_name', 'UNIQUE(name)', 'Il nome deve essere univoco!')
    ]

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Creatura",
    )

    image = fields.Image(
        string="Immagine",
    )

    ac = fields.Integer(
        string="Classe Armatura",
    )

    hp = fields.Integer(
        string="Punti Vita",
    )

    speed = fields.Integer(
        string="Velocita' m/r",
    )

    hd = fields.Char(
        string="Dadi Vita",
    )

    strength = fields.Integer(
        string="Forza",
    )

    dexterity = fields.Integer(
        string="Destrezza",
    )

    constitution = fields.Integer(
        string="Costituzione",
    )

    wisdom = fields.Integer(
        string="Saggezza",
    )

    intelligence = fields.Integer(
        string="Intelligenza",
    )

    charisma = fields.Integer(
        string="Carisma",
    )
