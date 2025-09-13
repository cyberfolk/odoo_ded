from odoo import models


class CreatureFaction(models.Model):
    _inherit = ['creature.faction', 'narrative.relation.mixin']
    _name = 'creature.faction'
