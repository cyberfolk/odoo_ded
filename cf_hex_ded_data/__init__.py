import logging
import base64
import os
from pathlib import Path

from odoo.exceptions import ValidationError

from . import models

_logger = logging.getLogger(__name__)
INIT_MODEL = [
    # model_name,                unique_fields, skip_fields'),
    ("biome.biome", 'name', 'creature_high_prob_ids,creature_low_prob_ids,encounter_ids,hex_ids'),
    ("structure.structure", 'name', ''),
    ("creature.tag", 'name', 'creature_ids'),
    ("creature.type", 'name', 'creature_ids'),
    ("creature.creature", 'name', ''),
    ("creature.npc", 'name', ''),
    ("creature.faction", 'name', ''),
    ("creature.encounter.line", 'name', 'encounter_ids'),
    ("creature.encounter", 'name', ''),
    ("hex.hex", 'name', ''),
]


def post_init__cf_hex_ded_data(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per popolare:
         - I biomi,
         - Le Strutture,
         - I Tag delle Creature,
         - I Tipi delle Creature,
         - Le Creature,
         - Le Fazioni,
         - Gli Scontri,
         - Gli Asset Tiles,
    """
    _logger.info("* START * post_init__cf_hex_ded_data()")
    env["asset.tile"].load_images()

    for model_name, unique_fields, skip_fields in INIT_MODEL:
        model = env['ir.model'].search([('model', '=', model_name)], limit=1)
        if not model:
            raise ValidationError(f"Modello non trovato: {model_name}")

        # region POPOLO CAMPI: UNIQUE, SKIP E SUPPORT
        model.support_field_fix('x_data_id', 'Data ID')
        model.support_field_fix('x_data_hash', 'Data Hash')
        model.write({
            'unique_fields_str': unique_fields,
            'skip_fields_str': skip_fields
        })
        # endregion

        # region RECUPERO DATI DA FILE
        nome_file = model_name.replace('.', '_') + '.json'
        file_path = (Path(__file__).resolve().parents[0] / 'data' / nome_file).as_posix()

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as file:
            binary_data = file.read()
            binary_data_encoded = base64.b64encode(binary_data).decode('utf-8')
        # endregion

        # region CREO/ESEGUO DATA-HANDLER
        handler = env['data.handler'].create({
            'name': f"INIT: {model_name}",
            'model_id': model.id,
            'datas_file': binary_data_encoded,
            'datas_file_name': f"{model_name}.json",
        })
        handler._onchange_datas_file()
        handler.start_import_from_zero()
        # endregion

    _logger.info("* END   * post_init__cf_hex_ded_data()")
