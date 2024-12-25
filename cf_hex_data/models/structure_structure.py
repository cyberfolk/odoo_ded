import logging

from odoo import models


class StructureStructure(models.Model):
    _name = "structure.structure"
    _inherit = ['structure.structure', 'mixin.import.py']

    @staticmethod
    def from_rec_to_dikt(rec):
        """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
        dikt = {
            'name': rec.name,
            'description': str(rec.description),
            'image': rec.image.decode('utf-8'),
            'biome_ids': [x.name for x in rec.biome_ids]
        }

        return dikt

    def _popolate_by_py(self, modulo):
        """OVERRIDE: ..."""
        data_dicts = getattr(modulo, 'dicts', None)
        if data_dicts is None:
            raise ValueError(f"'dicts' not found")

        LIST_ALREADY_EXIST = self.search([]).mapped('name')
        MAP_BIOME_ID = self.get_map_model_id('biome.biome')

        filtered_dicts = []
        for dikt in data_dicts:
            if dikt['name'] in LIST_ALREADY_EXIST:
                logging.warning(f"Il {self._name} {dikt['name']} esiste già")
                continue
            dikt['biome_ids'] = [MAP_BIOME_ID[x] for x in dikt['biome_ids']]
            dikt['image'] = dikt['image'].encode('utf-8')
            filtered_dicts.append(dikt)
        self.create(filtered_dicts)

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'biome_ids':   ('many2many', 'biome.biome'),
#     'description': ('html', None),
#     'image':       ('binary', None),
#     'name':        ('char', None)
# }
