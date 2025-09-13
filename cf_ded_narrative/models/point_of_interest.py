from odoo import models


class PointOfInterest(models.Model):
    _inherit = ['point.of.interest', 'narrative.relation.mixin']
    _name = 'point.of.interest'
