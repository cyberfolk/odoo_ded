from odoo import fields, models


class StructureStructure(models.Model):
    _name = "biome.structure"
    _description = "Struttura"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Struttura"
    )

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        string="Biomi",
        help="Biomi dove si può trovare la struttura"
    )
