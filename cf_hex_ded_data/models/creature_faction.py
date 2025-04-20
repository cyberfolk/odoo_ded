from odoo import models


class FactionFaction(models.Model):
    _name = "creature.faction"
    _inherit = ['creature.faction', 'mixin.import.json']
