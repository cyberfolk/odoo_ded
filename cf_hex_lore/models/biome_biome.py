from odoo import fields, models, api


class BiomeBiome(models.Model):
    _inherit = "biome.biome"

    hex_ids = fields.One2many(
        comodel_name="hex.hex",
        inverse_name="biome_id",
        string="Elenco degli Hex che hanno questo Bioma",
    )
