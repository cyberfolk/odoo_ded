from odoo import fields, models, api


class PointOfInterest(models.Model):
    _inherit = "point.of.interest"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="poi_hex_rel",
        string="HEXs",
    )
