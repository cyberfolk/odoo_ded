import logging

from odoo import fields, models, api, Command
from ...cf_hex_biome.utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureNpc(models.Model):
    _inherit = "creature.npc"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="creature_npc_hex_script_rel",
        string="Hexs possibili",
        help="Esagoni dove è possibile trovare l'NPC."
    )

    hex_id = fields.Many2many(
        comodel_name="hex.hex",
        string="Hex",
        help="Esagoni dove si trova attualmente l'NPC."
    )

