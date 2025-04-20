import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureNpcRoster(models.Model):
    _name = "creature.npc.roster"
    _description = "NPC Roster"

    name = fields.Char(
        string="Nome",
        required=True,
    )

    npc_ids = fields.Many2many(
        string="Elenco NPCs",
        comodel_name="creature.npc",
    )
