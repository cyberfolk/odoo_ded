import json

from odoo import api, fields, models
from ..utility.constant import MAP_TYPE_SELECTION


class Hex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.mixin']
    _description = "Hexagonal cell"

    name = fields.Char(
        string="Name",
        default=lambda self: self.code
    )

    quad_id = fields.Many2one(
        comodel_name='hex.quad',
        string="Quadrant",
    )

    map_id = fields.Many2one(
        related='quad_id.map_id',
        store=True,
    )

    border_N = fields.Many2one(
        comodel_name='hex.hex',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.hex',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.hex',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.hex',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.hex',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.hex',
        string="NW",
        help="Confine Nord-Ovest"
    )

    type = fields.Selection(
        selection=MAP_TYPE_SELECTION,
        string="Tipo",
        default="v1_19_q",
    )

    row = fields.Integer(
        string="Riga",
    )

    col = fields.Integer(
        string="Colonna",
    )

    @api.depends('index')
    def _compute_code(self):
        for rec in self:
            if rec.type == "v1_19_q" and rec.index:
                code = f"{rec.quad_id.code}"
                code += f".{str(rec.circle_order).zfill(2)}"
                code += f".{str(rec.circle_number).zfill(2)}"
            elif rec.type == "v2_nolimit_q":
                quad_row = rec.quad_id.row * 4
                quad_col = rec.quad_id.col * 4
                _row = rec.format_int_v2(quad_row + rec.row)
                _col = rec.format_int_v2(quad_col + rec.col)
                code = f"{_row}{_col}"
            else:
                code = 'void'
            rec.code = code
