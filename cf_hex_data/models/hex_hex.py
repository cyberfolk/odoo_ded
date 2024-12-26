import logging

from odoo import models

_logger = logging.getLogger(__name__)


class HexHex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.hex', 'mixin.import.py']

    # def get_data_json(self):
    #     """OVERRIDE: Recupera i dati del modello in una lista di dizionari.
    #       Ho fatto l'override per recuperare solo gli esagoni con lo satus 'script'."""
    #     _logger.info(f"START get_data_json ({self._name})")
    #
    #     records = self.search([('status', '=', 'script')])
    #     dicts = []
    #     for rec in records:
    #         dikt = self.from_rec_to_dikt(rec)
    #         dicts.append(dikt)
    #
    #     dat_str = f'dicts = {dicts}\n'
    #     _logger.info(f"END   get_data_json ({self._name})")
    #     return dat_str

    # @staticmethod
    # def from_rec_to_dikt(rec):
    #     """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
    #     dikt = {
    #         'name': rec.name,
    #         'status': 'script',
    #         'sml': rec.sml,
    #         'description': str(rec.description) if rec.description else '',
    #         'image': rec.image.decode('utf-8') if rec.image else '',
    #         'structure_id': rec.structure_id.name if rec.structure_id else False,
    #         'creature_id': rec.creature_id.name if rec.creature_id else False,
    #         'biome_id': rec.biome_id.name if rec.biome_id else False,
    #         'npc_ids': [x.name for x in rec.npc_ids],
    #         'faction_ids': [x.name for x in rec.faction_ids],
    #         # 'encounter_encounter_ids': [x.name for x in rec.encounter_encounter_ids],
    #         # 'image_gallery_ids': [x.name for x in rec.image_gallery_ids],
    #         # 'wild_encounter_ids': [x.name for x in rec.wild_encounter_ids],
    #     }
    #
    #     return dikt

    # def _popolate_by_py(self, modulo):
    #     """OVERRIDE: ..."""
    #     data_dicts = getattr(modulo, 'dicts', None)
    #     if data_dicts is None:
    #         raise ValueError(f"'dicts' not found")
    #
    #     LIST_ALREADY_EXIST = self.search([]).mapped('name')
    #     MAP_STRUCTURE_ID = self.get_map_model_id('structure.structure')
    #     MAP_CREATURE_ID = self.get_map_model_id('creature.creature')
    #     MAP_FACTION_ID = self.get_map_model_id('creature.faction')
    #     MAP_BIOME_ID = self.get_map_model_id('biome.biome')
    #     MAP_NPC_ID = self.get_map_model_id('creature.npc')
    #
    #     filtered_dicts = []
    #     for dikt in data_dicts:
    #         if dikt['name'] in LIST_ALREADY_EXIST:
    #             logging.warning(f"Il {self._name} {dikt['name']} esiste già")
    #             continue
    #
    #         dikt['structure_id'] = MAP_STRUCTURE_ID[dikt['structure_id']] if dikt['structure_id'] else False
    #         dikt['creature_id'] = MAP_CREATURE_ID[dikt['creature_id']] if dikt['creature_id'] else False
    #         dikt['faction_ids'] = [MAP_FACTION_ID.get(x) for x in dikt['faction_ids']] if dikt['faction_ids'] else False
    #         dikt['biome_id'] = MAP_BIOME_ID[dikt['biome_id']] if dikt['biome_id'] else False
    #         dikt['npc_ids'] = [MAP_NPC_ID.get(x) for x in dikt['faction_ids']] if dikt['faction_ids'] else False
    #         dikt['image'] = dikt.get('image').encode('utf-8') if dikt.get('image') else False
    #
    #         if not MAP_STRUCTURE_ID:
    #             dikt['structure_id'] = False
    #         if not MAP_CREATURE_ID:
    #             dikt['creature_id'] = False
    #         if not MAP_FACTION_ID:
    #             dikt['faction_ids'] = False
    #         if not MAP_BIOME_ID:
    #             dikt['biome_id'] = False
    #         if not MAP_NPC_ID:
    #             dikt['npc_ids'] = False
    #         filtered_dicts.append(dikt)
    #     self.create(filtered_dicts)

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#   'name':         ('char',        None),
#   'index':        ('integer',     None),
#   'type':         ('selection',   None),
#   'status':       ('selection',   None),
#   'row':          ('integer',     None),
#   'col':          ('integer',     None),
#   'sml':          ('integer',     None),
#   'description':  ('html',        None),
#   'image':        ('binary',      None),
#   'structure_id':             ('many2one',  'structure.structure'),
#   'creature_id':              ('many2one',  'creature.creature'),
#   'hex_asset_id':             ('many2one',  'hex.asset.tile')
#   'quad_id':                  ('many2one',  'hex.quad'),
#   'border_N':                 ('many2one',  'hex.hex'),
#   'border_NE':                ('many2one',  'hex.hex'),
#   'border_SE':                ('many2one',  'hex.hex'),
#   'border_S':                 ('many2one',  'hex.hex'),
#   'border_SW':                ('many2one',  'hex.hex'),
#   'border_NW':                ('many2one',  'hex.hex'),
#   'biome_id':                 ('many2one',  'biome.biome'),
#   'npc_ids':                  ('many2many', 'creature.npc'),
#   'faction_ids':              ('many2many', 'creature.faction'),
#   'image_gallery_ids':        ('many2many', 'ir.attachment'),
#   'wild_encounter_ids':       ('many2many', 'creature.encounter'),
#   'encounter_encounter_ids':  ('one2many',  'encounter.encounter'),
