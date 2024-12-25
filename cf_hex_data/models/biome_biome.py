from odoo import models


class BiomeBiome(models.Model):
    _name = "biome.biome"
    _inherit = ['biome.biome', 'mixin.import.py']

    @staticmethod
    def from_rec_to_dikt(rec):
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

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'name':            ('char',      None),
#     'color':           ('char',      None),
#     'state':           ('selection', None),
#     'cd_food':         ('integer',   None),
#     'cd_water':        ('integer',   None),
#     'cosmology':       ('selection', None),
#     'cd_navigation':   ('integer',   None),
#     'good_evil_axis':  ('selection', None),
#     'speed_of_travel': ('float',     None),
#     'hex_ids':                ('one2many',  'hex.hex'),
#     'structure_ids':          ('many2many', 'structure.structure'),
#     'encounter_ids':          ('many2many', 'creature.encounter'),
#     'creature_high_prob_ids': ('many2many', 'creature.creature'),
#     'creature_low_prob_ids':  ('many2many', 'creature.creature'),
# }
