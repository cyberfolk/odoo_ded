import logging

from odoo import models


class CreatureCreature(models.Model):
    _name = "creature.creature"
    _inherit = ['creature.creature', 'mixin.import.py']

    @staticmethod
    def from_rec_to_dikt(rec):
        """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
        dikt = {
            'name': rec.name,
            'cr': rec.cr,
            'image': rec.image.decode('utf-8'),
            'type_id': rec.type_id.name if rec.type_id else False,
            'tag_ids': [x.name for x in rec.tag_ids],
            'link_5et': rec.link_5et,
            'description': str(rec.description) if rec.description else '',
            'faction_ids': [x.name for x in rec.faction_ids],
            'biome_low_prob_ids': [x.name for x in rec.biome_low_prob_ids],
            'biome_high_prob_ids': [x.name for x in rec.biome_high_prob_ids],
        }

        return dikt

    def _popolate_by_py(self, modulo):
        """OVERRIDE: ..."""
        data_dicts = getattr(modulo, 'dicts', None)
        if data_dicts is None:
            raise ValueError(f"'dicts' not found")

        LIST_ALREADY_EXIST = self.search([]).mapped('name')
        MAP_TAG_ID = self.get_map_model_id('creature.tag')
        MAP_TYPE_ID = self.get_map_model_id('creature.type')
        MAP_FACTION_ID = self.get_map_model_id('creature.faction')
        MAP_BIOME_ID = self.get_map_model_id('biome.biome')

        filtered_dicts = []
        for dikt in data_dicts:
            if dikt['name'] in LIST_ALREADY_EXIST:
                logging.warning(f"Il {self._name} {dikt['name']} esiste già")
                continue
            dikt['type_id'] = MAP_TYPE_ID[dikt['type_id']] if dikt['type_id'] else False
            dikt['tag_ids'] = [MAP_TAG_ID[x] for x in dikt['tag_ids']]
            dikt['faction_ids'] = [MAP_FACTION_ID[x] for x in dikt['faction_ids']]
            dikt['biome_low_prob_ids'] = [MAP_BIOME_ID[x] for x in dikt['biome_low_prob_ids']]
            dikt['biome_high_prob_ids'] = [MAP_BIOME_ID[x] for x in dikt['biome_high_prob_ids']]
            dikt['image'] = dikt['image'].encode('utf-8')
            filtered_dicts.append(dikt)
        self.create(filtered_dicts)

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'name':                 ('char', None),
#     'cr':                   ('float', None),
#     'link_5et':             ('char', None),
#     'description':          ('html', None),
#     'image':                ('binary', None),
#     'tag_ids':              ('many2many', 'creature.tag'),
#     'type_id':              ('many2one', 'creature.type'),
#     'biome_high_prob_ids':  ('many2many', 'biome.biome'),
#     'biome_low_prob_ids':   ('many2many', 'biome.biome'),
#     'faction_ids':          ('many2many', 'creature.faction'),
# }
