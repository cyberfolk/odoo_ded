import json
from itertools import groupby

from odoo import models, api, Command


class BiomeBiome(models.Model):
    _inherit = "biome.biome"

    @api.model
    def get_json_biome_list(self):
        """Metodo richiamato dal orm di CurrentBiome.js
            :return: Json della lista di tutti i Biomi (in stato attivo) nel DB."""
        biome_fields = ['id', 'color', 'name', 'color_name_contrast']
        biome_list = self.env['biome.biome'].search([('state', '=', 'active')]).read(biome_fields)
        json_biome = json.dumps(biome_list)
        return json_biome
