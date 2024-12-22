import logging

from odoo.exceptions import ValidationError

from . import models

_logger = logging.getLogger(__name__)


def post_init_hook_cf_todo(env):
    try:
        _logger.info("* START * post_init_hook_cf_hex_data()")
        env["structure.structure"].popolate_by_csv()
        env["creature.tag"].popolate_by_csv()
        env["creature.type"].popolate_by_csv()
        env["creature.creature"].popolate_by_csv()
        env["creature.faction"].popolate_by_py()
        env["creature.encounter"].popolate_by_py()
        env["asset.tile"].load_images()
    except Exception as e:
        msg = (f"Errore nella funzione post_init_hook_cf_hex_data()\n"
               f"Fallito caricamento dei dati per il modulo cf_hex_biome\n"
               f"{e}")
        raise ValidationError(msg)
    finally:
        _logger.info("* END   * post_init_hook_cf_hex_data()")


from . import models
