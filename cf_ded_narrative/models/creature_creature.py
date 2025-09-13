from odoo import models


class CreatureCreature(models.Model):
    _inherit = ['creature.creature', 'narrative.relation.mixin']
    _name = 'creature.creature'
