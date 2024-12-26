from odoo import models


class CreatureType(models.Model):
    _name = "creature.type"
    _inherit = ['creature.type', 'mixin.import.json']

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'creature_ids': ('one2many', 'creature.creature'),
#     'name':         ('char', None),
# }
