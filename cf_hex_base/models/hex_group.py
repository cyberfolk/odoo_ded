from odoo import api, fields, models


class HexGroup(models.Model):
    _name = "hex.group"
    _description = "Gruppo di Hex"

    name = fields.Char(
        string="Name",
        default=lambda self: self.code
    )

    _sql_constraints = [
        ('unique_hex_group_name', 'UNIQUE(name)', 'Il nome del Gruppo di Hex deve essere univoco!')
    ]

    map_id = fields.Many2one(
        comodel_name='hex.map',
        string="Mappa",
    )

    hex_ids = fields.Many2many(
        comodel_name='hex.hex',
        string="Hexes",
    )

    color = fields.Char(
        string="Colore",
        help="Colore",
        default="#000000"
    )
