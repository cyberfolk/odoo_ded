from odoo import fields, models


class HexAssetTile(models.Model):
    _name = "hex.asset.tile"
    _description = "Hexagonal Asset Tiles"

    rotation = fields.Integer(string="Rotazione")
    asset_id = fields.Many2one(
        comodel_name='asset.tile',
        string="Asset",
        help="Assets contained in this hex"
    )
