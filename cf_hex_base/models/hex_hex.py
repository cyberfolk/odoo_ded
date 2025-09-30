from odoo import api, fields, models
from ..utility.selection import HEX_STATUS_SELECTION


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
        comodel_name='hex.map',
        string="Mappa",
    )

    status = fields.Selection(
        selection=HEX_STATUS_SELECTION,
        string="Status",
        default="script",
        help="Indica la status dell'Hex:\n"
             "[grid] -> Hex che appartiene a un Quadrante di una Mappa.\n"
             "[script] -> Hex scollegato da Quadranti e da Mappe. Usato per contenere Lore provvisorie."
    )

    # region FIELDS BORDI ----------------------------------------------------------------------------------------------
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

    # endregion --------------------------------------------------------------------------------------------------------
