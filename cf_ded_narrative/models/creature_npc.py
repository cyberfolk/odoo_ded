from odoo import models


class CreatureNPC(models.Model):
    _inherit = ['creature.creature', 'narrative.relation.mixin']
    _name = 'creature.creature'
