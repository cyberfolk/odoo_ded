import base64
import logging
import os
from pathlib import Path

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


def get_model(env, model_name):
    model = env['ir.model'].search([('model', '=', model_name)], limit=1)
    if not model:
        raise ValidationError(f"Modello non trovato: {model_name}")
    return model


def prepare_model_fields(model, unique_fields, skip_fields):
    """Configura i campi univoci e da saltare nel modello."""
    model.support_field_fix('x_data_id', 'Data ID')
    model.support_field_fix('x_data_hash', 'Data Hash')
    model.write({
        'unique_fields_str': unique_fields,
        'skip_fields_str': skip_fields
    })


def _load_file_as_base64(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File non trovato: {file_path}")
    with open(file_path, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')


def import_model_data(env, model, model_name):
    """Importa i dati da file JSON per un dato modello."""
    filename = f"{model_name.replace('.', '_')}.json"
    filepath = Path(__file__).resolve().parent.parent / 'data' / filename
    encoded_data = _load_file_as_base64(filepath)

    handler = env['data.handler'].create({
        'name': f"INIT: {model_name}",
        'model_id': model.id,
        'datas_file': encoded_data,
        'datas_file_name': filename,
    })
    handler._onchange_datas_file()
    handler.start_import_from_zero()
