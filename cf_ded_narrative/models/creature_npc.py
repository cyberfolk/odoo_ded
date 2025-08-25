from odoo import models


class CreatureNPC(models.Model):
    _inherit = ['creature.npc', 'narrative.relation.mixin']
    _name = 'creature.npc'
