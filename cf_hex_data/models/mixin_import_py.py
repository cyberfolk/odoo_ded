import importlib.util
import logging
import os
from pathlib import Path

from odoo import models

_logger = logging.getLogger(__name__)

EXCLUDED_FIELDS = {'write_date', 'write_uid', 'create_date', 'create_uid', 'display_name', 'id'}
MAP_MODEL_PY = {
    "structure.structure": "structure_structure.py",
    "creature.encounter": "creature_encounter.py",
    "creature.creature": "creature_creature.py",
    "creature.faction": "factions.py",
    "creature.type": "creature_type.py",
    "creature.tag": "creature_tag.py",
    "biome.biome": "biome_biome.py",
}


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
        nome_file = MAP_MODEL_PY.get(self._name)
        if not nome_file:
            raise ValueError(f"No file mapping found for model {self._name}")
        return (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

    def get_map_model_id(self, model_name):
        model_records = self.env[model_name].search([])
        MAP_MODEL_ID = {x.name: x.id for x in model_records}
        return MAP_MODEL_ID

    def get_fields_dict(self):
        fields_dict = {}
        for name, field in self._fields.items():
            if name in EXCLUDED_FIELDS or field.compute or field.related:
                continue
            fields_dict[name] = (field.type, field.comodel_name)
            # fields_dict[name] = {
            #     # 'type': field.type,
            #     # 'comodel_name': field.comodel_name,
            #     # 'readonly': field.readonly,
            #     # 'default': field.default,
            #     # 'domain': field.get('domain'),
            #     # 'string': field.string,
            # }
        return fields_dict

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

    def from_rec_to_dikt(self, rec):
        """Da ereditare nei modelli che implementano il mixin.
            Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""

        dikt = {'name': rec.name, }

        return dikt
    # endregion --------------------------------------------------------------------------------------------------------
