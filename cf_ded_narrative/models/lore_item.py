from odoo import fields, models


class LoreItem(models.Model):
    _inherit = ['lore.item', 'narrative.relation.mixin']
    _name = 'lore.item'
