import logging

from .utility import utility

_logger = logging.getLogger(__name__)

# Modelli da inizializzare: (modello, campi unici, campi da ignorare)
INIT_MODELS = [
    ("lore.item",               'name', ''),
    ("hex.hex",                 'name', ''),
]


def post_init__cf_hex_ded_data_finimondo(env):
    """
    Eseguito post-installazione modulo.
    Inizializza i dati dei modelli:
    """
    _logger.info("* START * post_init__cf_hex_ded_data_finimondo()")

    # Configurazione modelli
    for model_name, unique_fields, skip_fields in INIT_MODELS:
        model = utility.get_model(env, model_name)
        utility.prepare_model_fields(model, unique_fields, skip_fields)

    # Importazione dati modelli
    for model_name, _, _ in INIT_MODELS:
        model = utility.get_model(env, model_name)
        utility.import_model_data(env, model, model_name)

    _logger.info("* END   * post_init__cf_hex_ded_data_finimondo()")
