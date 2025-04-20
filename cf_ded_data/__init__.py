import logging

from odoo.exceptions import ValidationError

from . import models

_logger = logging.getLogger(__name__)


def post_init_hook_cf_hex_data(env):
    """Viene eseguito dopo l'installazione del modulo. Serve per popolare:
         - I biomi,
         - Le Strutture,
         - I Tag delle Creature,
         - I Tipi delle Creature,
         - Le Creature,
         - Le Fazioni,
         - Gli Scontri,
    """
    try:
        _logger.info("* START * post_init_hook_cf_hex_data()")
        env["data.handler"].initialize(model_name='biome.biome', unique_field="name")
        env["data.handler"].initialize(model_name='structure.structure', unique_field="name")
        env["data.handler"].initialize(model_name='creature.tag', unique_field="name")
        env["data.handler"].initialize(model_name='creature.type', unique_field="name")
        env["data.handler"].initialize(model_name='creature.creature', unique_field="name")
        env["data.handler"].initialize(model_name='creature.faction', unique_field="name, code")
        env["data.handler"].initialize(model_name='creature.encounter', unique_field="name")
    except Exception as e:
        msg = (f"Errore nella funzione post_init_hook_cf_hex_data()\n"
               f"Fallito caricamento dei dati per il modulo cf_hex_biome\n"
               f"{e}")
        raise ValidationError(msg)
    finally:
        _logger.info("* END   * post_init_hook_cf_hex_data()")
