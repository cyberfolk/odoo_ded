from odoo import fields, models


class SettlementSettlement(models.Model):
    _inherit = ['settlement.settlement', 'narrative.relation.mixin']
    _name = 'settlement.settlement'
