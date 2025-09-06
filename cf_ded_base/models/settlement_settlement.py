from odoo import fields, models

SCALE_SELECTION_LIST = [
    ("borgo", "Borgo"),
    ("villaggio", "Villaggio"),
    ("citta", "Città"),
    ("capitale", "Capitale"),
    ("megalopoli", "Megalopoli"),
    ("avamposto", "Avamposto"),
    ("eremo", "Eremo"),
]
ATTITUDE_SELECTION_LIST = [
    ("cordiale", "Cordiale"),
    ("neutrale", "Neutrale"),
    ("ostile", "Ostile")
]


class Settlement(models.Model):
    _name = "settlement.settlement"
    _description = "Insediamento"

    name = fields.Char(
        string="Nome",
        required=True
    )
    description = fields.Html(
        string="Descrizione"
    )
    scale = fields.Selection(
        selection=SCALE_SELECTION_LIST,
        string="Scala",
        required=True,
        default="borgo",
    )
    attitude = fields.Selection(
        selection=ATTITUDE_SELECTION_LIST,
        string="Atteggiamento",
        required=True,
        default="neutrale",
    )
    needs = fields.Text(
        string="Bisogni"
    )
    offers = fields.Text(
        string="Offre"
    )
    image = fields.Image(
        string="Immagine",
    )
