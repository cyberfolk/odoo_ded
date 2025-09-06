from odoo import fields, models, api


class PointOfInterest(models.Model):
    _inherit = "point.of.interest"
    _description = "Point of Interest"

    hex_ids = fields.Many2many(
        string="Esagoni",
        comodel_name="hex.hex",
        relation="point_of_interest_hex_rel",
    )
