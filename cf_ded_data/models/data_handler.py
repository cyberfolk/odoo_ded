import json
import logging
import os
from pathlib import Path

from odoo import models, api

_logger = logging.getLogger(__name__)


class MixinImportJson(models.AbstractModel):
    _name = 'data.handler'
    _description = 'Mixin per popolare i modelli da Json'

    def initialize(self, model_name, unique_field):
        """Crea record partendo dal file '.json' nella cartella 'data'."""
        _logger.info(f"** START ** initialize() - ({self._name})")
        try:
            file_path = self._get_file_path()
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            handler = self.create(
                {
                    'name': f"INIT {model_name}",
                    'datas': json.dumps(json_data),
                    'model_id': self.env['ir.model'].search([('model', '=', model_name)]).id
                }
            )
            if handler.error_unique_field:
                pass

            if handler.error_x_data_id_field:
                handler.fix_error_x_data_id_field()

            if handler.error_x_data_hash_field:
                handler.fix_error_x_data_hash_field()

            handler.start_import_from_zero()

        except json.JSONDecodeError as e:
            _logger.error(f"** ERROR ** Failed to decode JSON: {e}")
        except FileNotFoundError as e:
            _logger.error(f"** ERROR ** File not found: {e}")
        except Exception as e:
            _logger.error(f"** ERROR ** initialize() - ({self._name})")
            _logger.exception(e)
        finally:
            _logger.info(f"** END   ** initialize() - ({self._name})")

    # region UTILITY ---------------------------------------------------------------------------------------------------
    def _get_file_path(self):
        """Helper method to get the file path based on the model name."""
        nome_file = self._name.replace('.', '_') + '.json'
        return (Path(__file__).resolve().parents[1] / 'data' / nome_file).as_posix()

