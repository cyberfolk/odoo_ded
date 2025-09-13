import logging

from odoo import fields, models, api, Command
from ...cf_ded_base.utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureCreature(models.Model):
    _inherit = "creature.creature"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="creature_hex_script_rel",
        string="HEXs",
        help="Esagoni dove è possibile trovarlo."
    )

    hex_id = fields.Many2many(
        comodel_name="hex.hex",
        string="Hex",
        help="Esagoni dove si trova attualmente l'NPC."
    )

