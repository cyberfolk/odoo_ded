from odoo import fields, models


class StructureStructure(models.Model):
    _name = "structure.structure"
    _description = "Struttura"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Struttura"
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della fazione",
    )

    image = fields.Image(
        string="Immagine",
    )

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        string="Biomi",
        help="Biomi dove si può trovare la struttura"
    )
