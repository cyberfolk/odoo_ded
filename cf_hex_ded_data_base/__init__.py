import logging

from . import models
from .utility import utility

_logger = logging.getLogger(__name__)

# Modelli da inizializzare: (modello, campi unici, campi da ignorare)
INIT_MODELS = [
    ("artifact.artifact",       'name', 'creature_high_prob_ids,creature_low_prob_ids,encounter_ids,hex_ids'),
    ("biome.biome",             'name', 'creature_high_prob_ids,creature_low_prob_ids,encounter_ids,hex_ids'),
    ("biome.structure",         'name', ''),
    ("creature.tag",            'name', 'creature_ids'),
    ("creature.type",           'name', 'creature_ids'),
    ("creature.creature",       'name', ''),
    ("creature.faction",        'name', ''),
    ("creature.faction.tag",    'name', ''),
    ("creature.encounter.line", 'name', 'encounter_ids'),
    ("creature.encounter",      'name', ''),
    ("point.of.interest",       'name', ''),
    ("quest.quest",             'name', ''),
    ("settlement.settlement",   'name', ''),
]


def post_init__cf_hex_ded_data_base(env):
    """
    Eseguito post-installazione modulo.
    Inizializza i dati dei modelli:
        - Biomi
        - Strutture
        - Tag delle Creature
        - Tipi delle Creature
        - Creature
        - Fazioni
        - Scontri
        - Asset Tiles
    """
    _logger.info("* START * post_init__cf_hex_ded_data_base()")

    # Caricamento immagini tile
    env["asset.tile"].load_images()

    # Configurazione modelli
    for model_name, unique_fields, skip_fields in INIT_MODELS:
        model = utility.get_model(env, model_name)
        utility.prepare_model_fields(model, unique_fields, skip_fields)

    # Importazione dati modelli
    for model_name, _, _ in INIT_MODELS:
        model = utility.get_model(env, model_name)
        utility.import_model_data(env, model, model_name)

    _logger.info("* END   * post_init__cf_hex_ded_data_base()")
