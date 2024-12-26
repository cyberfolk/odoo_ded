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

    def get_dict_map_model_id(self):
        DICT_MAP_MODEL_ID = {}
        for f_name, f_info in self._fields.items():
            comodel_name = f_info.comodel_name
            if comodel_name:
                DICT_MAP_MODEL_ID[comodel_name] = self.get_map_model_id(comodel_name)
        return DICT_MAP_MODEL_ID
    # endregion

    # region DA EREDITARE ALL'OCCORRENZA NEI MIXIN ---------------------------------------------------------------------
    def _popolate_by_py(self, modulo):
        """Da ereditare nei modelli che implementano il mixin."""
        data_dicts = getattr(modulo, 'dicts', None)
        if data_dicts is None:
            raise ValueError(f"'dicts' not found")

        LIST_ALREADY_EXIST = self.search([]).mapped('name')
        DICT_MAP_MODEL_ID = self.get_dict_map_model_id()

        filtered_dicts = []
        for dikt in data_dicts:
            if dikt['name'] in LIST_ALREADY_EXIST:
                logging.warning(f"Il {self._name} {dikt['name']} esiste già")
                continue
            for f_name, f_info in self._fields.items():  # f_name  -> field_name, f_info -> field_info
                f_value = dikt.get(f_name)               # f_value -> field_value
                f_type = f_info.type                     # f_type  -> field_type
                f_comodel = f_info.comodel_name
                MAP_MODEL_ID = DICT_MAP_MODEL_ID.get(f_comodel)
                if f_name in EXCLUDED_FIELDS or f_info.compute or f_info.related:
                    continue
                elif f_type in ['binary']:
                    dikt[f_name] = dikt.get('image').encode('utf-8') if dikt.get('image') else False
                elif f_type in ['many2one']:
                    dikt[f_name] = MAP_MODEL_ID.get(f_value) if f_value else False
                elif f_type in ['many2many', 'one2many']:
                    dikt[f_name] = [MAP_MODEL_ID.get(x) for x in f_value] if f_value else False
                    dikt[f_name] = clean_list(dikt[f_name])

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

    @staticmethod
    def from_rec_to_dikt(rec):
        """Da ereditare nei modelli che implementano il mixin.
            Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""

        dikt = {}
        for f_name, f_info in rec._fields.items():  # f_name  -> field_name, f_info -> field_info
            f_value = rec[f_name]                   # f_value -> field_value
            f_type = f_info.type                    # f_type  -> field_type

            if f_name in EXCLUDED_FIELDS or f_info.compute or f_info.related:
                continue
            elif f_type in ['binary']:
                dikt[f_name] = f_value.decode('utf-8') if f_value else ''
            elif f_type in ['html']:
                dikt['description'] = str(f_value) if f_value else ''
            elif f_type in ['many2one']:
                dikt[f_name] = f_value.name if f_value else False
            elif f_type in ['many2many', 'one2many']:
                dikt[f_name] = [x.name for x in f_value] if f_value else []
            else:
                dikt[f_name] = f_value

        return dikt
    # endregion --------------------------------------------------------------------------------------------------------


def clean_list(_list):
    """Rimuove tutti i valori None da una lista e ritorna la lista filtrata.
        Se la lista risultante è vuota, ritorna False. """
    if not _list:
        return False
    if not isinstance(_list, list):
        raise ValueError("Il parametro deve essere una lista.")
    filtered_list = [x for x in _list if x is not None]  # Filtra i valori None
    return filtered_list if filtered_list else False  # Ritorna None se la lista filtrata è vuota
