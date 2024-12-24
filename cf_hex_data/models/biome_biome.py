from odoo import models


class BiomeBiome(models.Model):
    _name = "biome.biome"
    _inherit = ['biome.biome', 'mixin.import.py']

    def from_rec_to_dikt(self, rec):
        """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
        dikt = {
            'name': rec.name,
            'color': rec.color,
            'state': rec.state,
            'cd_food': rec.cd_food,
            'cd_water': rec.cd_water,
            'cosmology': rec.cosmology,
            'cd_navigation': rec.cd_navigation,
            'good_evil_axis': rec.good_evil_axis,
            'speed_of_travel': rec.speed_of_travel,
        }

        return dikt
