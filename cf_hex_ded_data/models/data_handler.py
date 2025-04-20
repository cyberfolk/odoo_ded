import base64
import logging
import os
from pathlib import Path

from odoo import models, api

_logger = logging.getLogger(__name__)
INIT_MODEL = [
    "biome.biome",
    "structure.structure",
    "creature.tag",
    "creature.type",
    "creature.creature",
    "creature.faction",
    "creature.encounter.line",
    "creature.encounter",
    "hex.hex",
]


class DataHandler(models.AbstractModel):
    _inherit = 'data.handler'
    _description = 'Mixin per popolare i modelli da Json'

    def init_data_handler_fields(self):
        for model_name in INIT_MODEL:
            handler = self.create({
                'name': f"INIT: {model_name}",
                'model_id': self.env['ir.model'].search([('model', '=', model_name)], limit=1).id,
                'datas_file': self._get_datas_file(model_name),
                'datas_file_name': f"{model_name}.json",
            })
            handler._onchange_datas_file()
            handler.start_import_from_zero()
            pass

    def _get_datas_file(self, model_name):
        """Crea record partendo dal file '.json' nella cartella 'data'."""
        _logger.info(f"** START ** popolate_by_json() - ({model_name})")
        try:
            file_path = self._get_file_path(model_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'rb') as file:
                binary_data = file.read()
                binary_data_encoded = base64.b64encode(binary_data).decode('utf-8')  # Questa stringa è valida

            return binary_data_encoded

        except FileNotFoundError as e:
            _logger.error(f"** ERROR ** File not found: {e}")
        except Exception as e:
            _logger.error(f"** ERROR ** _get_datas_file() - ({model_name})")
            _logger.exception(e)
        finally:
            _logger.info(f"** END   ** _get_datas_file() - ({model_name})")

    # region UTILITY ---------------------------------------------------------------------------------------------------
    def _get_file_path(self, model_name):
        """Helper method to get the file path based on the model name."""
        nome_file = model_name.replace('.', '_') + '.json'
        return (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

    # def get_comodel_map(self):
#         COMODEL_MAP = {}
#         for f_name, f_info in self._fields.items():
#             comodel_name = f_info.comodel_name
#             if comodel_name:
#                 comodel_records = self.env[comodel_name].search([])
#                 MAP_MODEL_ID = {x.name: x.id for x in comodel_records}
#                 COMODEL_MAP[comodel_name] = MAP_MODEL_ID
#         return COMODEL_MAP
#
#     # endregion
#
#     # region DA EREDITARE ALL'OCCORRENZA NEI MIXIN ---------------------------------------------------------------------
#     def _popolate_by_json(self, data_dicts):
#         """Da ereditare nei modelli che implementano il mixin."""
#
#         LIST_ALREADY_EXIST = self.search([]).mapped('name')
#         COMODEL_MAP = self.get_comodel_map()
#
#         for dikt in data_dicts:
#             if dikt.get('name') in LIST_ALREADY_EXIST:
#                 logging.warning(f"Il {self._name} {dikt['name']} esiste già")
#                 continue
#             for f_name, f_info in self._fields.items():  # f_name  -> field_name, f_info -> field_info
#                 f_value = dikt.get(f_name)  # f_value -> field_value
#                 f_type = f_info.type  # f_type  -> field_type
#                 f_comodel = f_info.comodel_name
#                 MAP_MODEL_ID = COMODEL_MAP.get(f_comodel)
#                 if f_name in EXCLUDED_FIELDS or f_info.compute or f_info.related:
#                     continue
#                 elif f_type in ['binary']:
#                     dikt[f_name] = dikt.get('image').encode('utf-8') if dikt.get('image') else False
#                 elif f_type in ['many2one']:
#                     dikt[f_name] = MAP_MODEL_ID.get(f_value) if f_value else False
#                 elif f_type in ['many2many', 'one2many']:
#                     dikt[f_name] = [MAP_MODEL_ID.get(x) for x in f_value] if f_value else False
#                     dikt[f_name] = clean_list(dikt[f_name])
#
#             rec = self.create(dikt)
#             if self._name in COMODEL_MAP:
#                 COMODEL_MAP[self._name][rec.name] = rec.id
#
#     def get_data_json(self):
#         """Da ereditare nei modelli che implementano il mixin.
#         Recupera i dati del modello in una lista di dizionari."""
#         _logger.info(f"START get_data_json ({self._name})")
#
#         restrict_domain = self.get_restrict_domain()
#         records = self.search(restrict_domain)
#         dicts = []
#         for rec in records:
#             dikt = self.from_rec_to_dikt(rec)
#             dicts.append(dikt)
#
#         dicts_json = json.dumps(dicts, indent=4, ensure_ascii=False)
#         _logger.info(f"END   get_data_json ({self._name})")
#         return dicts_json
#
#     @staticmethod
#     def from_rec_to_dikt(rec):
#         """Da ereditare nei modelli che implementano il mixin.
#             Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
#
#         dikt = {}
#         for f_name, f_info in rec._fields.items():  # f_name  -> field_name, f_info -> field_info
#             f_value = rec[f_name]  # f_value -> field_value
#             f_type = f_info.type  # f_type  -> field_type
#
#             if (f_name in EXCLUDED_FIELDS or f_info.compute or f_info.related) and f_name != 'name':
#                 continue
#             elif f_type in ['binary']:
#                 dikt[f_name] = f_value.decode('utf-8') if f_value else ''
#             elif f_type in ['html']:
#                 dikt['description'] = str(f_value) if f_value else ''
#             elif f_type in ['many2one']:
#                 dikt[f_name] = f_value.name if f_value else False
#             elif f_type in ['many2many', 'one2many']:
#                 dikt[f_name] = [x.name for x in f_value] if f_value else []
#             else:
#                 dikt[f_name] = f_value
#
#         return dikt
#
#     @staticmethod
#     def get_restrict_domain():
#         """Da ereditare nei modelli che implementano il mixin."""
#         return []
#
#     # endregion --------------------------------------------------------------------------------------------------------
#
#     @api.model
#     def trigger_stored_compute(self):
#         # Ottieni tutti i campi del modello corrente
#         fields_to_compute = [
#             field_name for field_name, field in self._fields.items()
#             if field.store and field.compute
#         ]
#
#         if fields_to_compute:
#             # Forza il ricalcolo dei campi
#             for record in self:
#                 record.write({field: record[field] for field in fields_to_compute})
#
#
# def clean_list(_list):
#     """Rimuove tutti i valori None da una lista e ritorna la lista filtrata.
#         Se la lista risultante è vuota, ritorna False. """
#     if not _list:
#         return False
#     if not isinstance(_list, list):
#         raise ValueError("Il parametro deve essere una lista.")
#     filtered_list = [x for x in _list if x is not None]  # Filtra i valori None
#     return filtered_list if filtered_list else False  # Ritorna None se la lista filtrata è vuota
