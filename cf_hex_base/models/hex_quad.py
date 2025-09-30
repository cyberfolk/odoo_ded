from odoo import api, fields, models, Command


class Quadrant(models.Model):
    _name = "hex.quad"
    _inherit = ['hex.mixin']
    _description = "Quadrant, contains Hexagons."

    map_id = fields.Many2one(
        comodel_name='hex.map',
        string="Mappa",
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        string="Hexes",
        inverse_name='quad_id',
    )

    hook_widget = fields.Char(
        string="hook_widget",
        help="Usato solamente per agganciare il widget del quadrante."
    )

    # Campi usati sia da v2 che v3
    row = fields.Integer(string="Riga")
    col = fields.Integer(string="Colonna")

    # region FIELDS BORDI --------------------------------------------------------------------------------------------
    border_N = fields.Many2one(
        comodel_name='hex.quad',
        string="N",
        help="Confine Nord"
    )

    border_NE = fields.Many2one(
        comodel_name='hex.quad',
        string="NE",
        help="Confine Nord-Est"
    )

    border_SE = fields.Many2one(
        comodel_name='hex.quad',
        string="SE",
        help="Confine Sud-Est"
    )

    border_S = fields.Many2one(
        comodel_name='hex.quad',
        string="S",
        help="Confine Sud"
    )

    border_SW = fields.Many2one(
        comodel_name='hex.quad',
        string="SW",
        help="Confine Sud-Ovest"
    )

    border_NW = fields.Many2one(
        comodel_name='hex.quad',
        string="NW",
        help="Confine Nord-Ovest"
    )

    # endregion ------------------------------------------------------------------------------------------------------

    def unlink(self):
        for rec in self:
            for hex in rec.hex_ids:
                hex.unlink()
        return super(Quadrant, self).unlink()
