import importlib.util
import logging
import os
from pathlib import Path

from odoo import models

_logger = logging.getLogger(__name__)

EXCLUDED_FIELDS = {'write_date', 'write_uid', 'create_date', 'create_uid', 'display_name', 'id'}


class MixinImportPy(models.AbstractModel):
    _name = 'mixin.import.py'
    _description = 'Mixin per popolare i vari modelli da python'

    def download_data_py(self):
        """Scarica i dati del modello in un file '.py' mettendolo nella cartella 'data'."""
        _logger.info(f"START download_data_py ({self._name})")

        data_str = self.get_data_str()
        file_path = self._get_file_path()

        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(data_str)
        except IOError as e:
            _logger.error(f"Failed to write to {file_path}: {e}")
        finally:
            _logger.info(f"END download_data_py ({self._name})")

    def popolate_by_py(self):
        """Crea record partendo dal file '.py' nella cartella 'data'."""
        _logger.info(f"** START ** popolate_by_py() - ({self._name})")
        try:
            file_path = self._get_file_path()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            spec = importlib.util.spec_from_file_location(Path(file_path).stem, file_path)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            self._popolate_by_py(modulo)

        except FileNotFoundError as e:
            _logger.error(f"** ERROR ** File not found: {e}")
        except Exception as e:
            _logger.error(f"** ERROR ** popolate_by_py() - ({self._name})")
            _logger.exception(e)
        finally:
            _logger.info(f"** END   ** popolate_by_py() - ({self._name})")

    # region UTILITY ---------------------------------------------------------------------------------------------------
    def _get_file_path(self):
        """Helper method to get the file path based on the model name."""
        nome_file = self._name.replace('.', '_') + '.py'
        if not nome_file:
            raise ValueError(f"No file mapping found for model {self._name}")
        return (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

    def get_map_model_id(self, model_name):
        model_records = self.env[model_name].search([])
        MAP_MODEL_ID = {x.name: x.id for x in model_records}
        return MAP_MODEL_ID

    def get_fields_dict(self):
        """Ritorna un dict[campo: (tipo, comodel)] e un dict[categoria: [lista campi]]."""
        fields_dict = {}
        group_fields = {
            'base': [],
            'one2many': [],
            'many2one': [],
            'many2many': []
        }

        for field_name, field in self._fields.items():
            # Ignora i campi esclusi o quelli con compute/related
            if field_name in EXCLUDED_FIELDS or field.compute or field.related:
                continue

            # Aggiungi al dizionario dei campi
            fields_dict[field_name] = (field.type, field.comodel_name)

            # Classifica il campo in base al tipo
            if field.type in group_fields:
                group_fields[field.type].append(field_name)
            else:
                group_fields['base'].append(field_name)

        return fields_dict, group_fields

    # endregion

    # region DA EREDITARE ALL'OCCORRENZA NEI MIXIN ---------------------------------------------------------------------
    def _popolate_by_py(self, modulo):
        """Da ereditare nei modelli che implementano il mixin."""
        data_dicts = getattr(modulo, 'dicts', None)
        if data_dicts is None:
            raise ValueError(f"'dicts' not found")

        LIST_ALREADY_EXIST = self.search([]).mapped('name')

        filtered_dicts = []
        for dikt in data_dicts:
            if dikt['name'] in LIST_ALREADY_EXIST:
                logging.warning(f"Il {self._name} {dikt['name']} esiste già")
                continue
            filtered_dicts.append(dikt)
        self.create(filtered_dicts)

        # data_dicts = getattr(modulo, 'dicts', None)
        # if data_dicts is None:
        #     raise ValueError(f"'dicts' not found")
        # LIST_ALREADY_EXIST = self.search([]).mapped('name')
        # MAP_TAG_ID         = self.get_map_model_id('creature.tag')
        # MAP_TYPE_ID        = self.get_map_model_id('creature.type')
        # MAP_FACTION_ID     = self.get_map_model_id('creature.faction')
        # MAP_BIOME_ID       = self.get_map_model_id('biome.biome')
        # MAP_STRUCTURE_ID   = self.get_map_model_id('structure.structure')
        #
        # filtered_dicts = []
        # for dikt in data_dicts:
        #     if dikt['name'] in LIST_ALREADY_EXIST:
        #         logging.warning(f"Il {self._name} {dikt['name']} esiste già")
        #         continue
        #
        #     dikt['type_id']             = MAP_TYPE_ID[dikt['type_id']] if dikt.get('type_id') else False
        #     dikt['structure_ids']       = [MAP_STRUCTURE_ID.get(x) for x in dikt['structure_ids']]       if dikt.get('structure_ids')       else False
        #     dikt['tag_ids']             = [MAP_TAG_ID.get(x)       for x in dikt['tag_ids']]             if dikt.get('tag_ids')             else False
        #     dikt['faction_ids']         = [MAP_FACTION_ID.get(x)   for x in dikt['faction_ids']]         if dikt.get('faction_ids')         else False
        #     dikt['biome_low_prob_ids']  = [MAP_BIOME_ID.get(x)     for x in dikt['biome_low_prob_ids']]  if dikt.get('biome_low_prob_ids')  else False
        #     dikt['biome_high_prob_ids'] = [MAP_BIOME_ID.get(x)     for x in dikt['biome_high_prob_ids']] if dikt.get('biome_high_prob_ids') else False
        #     dikt['image']               = dikt.get('image').encode('utf-8') if dikt.get('image') else False
        #
        #     if not MAP_STRUCTURE_ID:
        #         dikt['structure_ids'] = False
        #     if not MAP_TAG_ID:
        #         dikt['tag_ids'] = False
        #     if not MAP_TYPE_ID:
        #         dikt['type_id'] = False
        #     if not MAP_FACTION_ID:
        #         dikt['faction_ids'] = False
        #     if not MAP_BIOME_ID:
        #         dikt['biome_low_prob_ids'] = False
        #         dikt['biome_high_prob_ids'] = False
        #
        #     if 'structure_ids' not in list(self._fields.keys()):
        #         dikt.pop('structure_ids')
        #     if 'tag_ids' not in list(self._fields.keys()):
        #         dikt.pop('tag_ids')
        #     if 'type_id' not in list(self._fields.keys()):
        #         dikt.pop('type_id')
        #     if 'faction_ids' not in list(self._fields.keys()):
        #         dikt.pop('faction_ids')
        #     if 'biome_low_prob_ids' not in list(self._fields.keys()):
        #         dikt.pop('biome_low_prob_ids')
        #     if 'biome_high_prob_ids' not in list(self._fields.keys()):
        #         dikt.pop('biome_high_prob_ids')
        #     if 'image' not in list(self._fields.keys()):
        #         dikt.pop('image')
        #
        #     filtered_dicts.append(dikt)
        # self.create(filtered_dicts)

    def get_data_str(self):
        """Da ereditare nei modelli che implementano il mixin.
        Recupera i dati del modello in una lista di dizionari."""
        _logger.info(f"START get_data_str ({self._name})")

        records = self.search([])
        dicts = []
        for rec in records:
            dikt = self.from_rec_to_dikt(rec)
            dicts.append(dikt)

        dat_str = f'dicts = {dicts}\n'
        _logger.info(f"END   get_data_str ({self._name})")
        return dat_str

    @staticmethod
    def from_rec_to_dikt(rec):
        """Da ereditare nei modelli che implementano il mixin.
            Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""

        dikt = {'name': rec.name, }
        # dikt = {}
        # for name in rec.fields_get():  # name -> field_name
        #     value = rec[name]   # value -> field_value
        #
        #     if name == 'image':
        #         dikt['image'] = value.decode('utf-8') if value else '',
        #     elif name == 'description':
        #         dikt['description'] = str(value) if value else '',
        #     elif name in group_fields['base']:
        #         dikt[name] = value
        #     elif name in group_fields['many2one']:
        #         dikt[name] = value.name if value else False
        #     elif name in group_fields['many2many']:
        #         dikt[name] = [x.name for x in value] if value else []
        #     elif name in group_fields['one2many']:
        #         dikt[name] = [x.name for x in value] if value else []

        return dikt
    # endregion --------------------------------------------------------------------------------------------------------
