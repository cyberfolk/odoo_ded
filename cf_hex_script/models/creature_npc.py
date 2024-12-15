import logging

from odoo import fields, models, api, Command
from ...cf_hex_biome.utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureNpc(models.Model):
    _inherit = "creature.npc"
    _description = "NPC"

    hex_script_ids = fields.Many2many(
        comodel_name="hex.script",
        relation="creature_npc_hex_script_rel",
        string="Hex Script",
        help="Esagoni Scriptati dove è possibile trovare l'NPC."
    )
