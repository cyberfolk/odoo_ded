from odoo import fields, models, api, Command


class HexMap(models.Model):
    _name = "hex.map"
    _description = "Mappa, contains Quadrants."

    name = fields.Char(
        string='Name',
    )

    quad_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='map_id',
    )

    type = fields.Selection(
        selection=[],
        string="Tipo",
    )
