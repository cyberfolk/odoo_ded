import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class CreatureRoster(models.Model):
    _name = "creature.roster"
    _description = "Creature Roster"

    name = fields.Char(
        string="Nome",
        required=True,
    )

    creature_ids = fields.Many2many(
        string="Elenco Creature",
        comodel_name="creature.creature",
    )
