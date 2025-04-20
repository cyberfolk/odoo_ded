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
         - Gli Asset Tiles,
    """
    try:
        _logger.info("* START * post_init_hook_cf_hex_data()")
        env['ir.model'].init_data_handler_fields()
        env['data.handler'].init_data_handler_fields()
        # env["biome.biome"].popolate_by_json()
        # env["structure.structure"].popolate_by_json()
        # env["creature.tag"].popolate_by_json()
        # env["creature.type"].popolate_by_json()
        # env["creature.creature"].popolate_by_json()
        # env["creature.faction"].popolate_by_json()
        # env["creature.encounter"].popolate_by_json()
        # env["hex.hex"].popolate_by_json()
        # env["asset.tile"].load_images()
    except Exception as e:
        msg = (f"Errore nella funzione post_init_hook_cf_hex_data()\n"
               f"{e}")
        raise ValidationError(msg)
    finally:
        _logger.info("* END   * post_init_hook_cf_hex_data()")
