import json

from odoo import api, fields, models


class Hex(models.Model):
    _inherit = "hex.hex"
    _description = "Hexagonal cell"

    hex_asset_id = fields.Many2one(
        comodel_name='hex.asset.tile',
        string="Hex Asset",
        help="Hex Assets contained in this hex"
    )

    @api.model
    def change_hex_biome(self, hex_id, biome_id):
        """Metodo richiamato dal orm di view_map.js
           Setta il campo biome_id del di hex_id"""
        _hex = self.env['hex.hex'].browse(hex_id)
        _hex.biome_id = biome_id

    @api.model
    def set_asset_tiles(self, hex_id, current_tile):
        """Metodo richiamato dal orm di view_map.js
           Setta i parametri di hex_asset su hex_id"""
        _hex = self.env['hex.hex'].browse(hex_id)
        hex_asset_vals = {
            'asset_id': current_tile['tile_id'],
            'rotation': current_tile['rotation']
        }
        if not _hex.hex_asset_id:
            hex_asset = self.env['hex.asset.tile'].create(hex_asset_vals)
            _hex.hex_asset_id = hex_asset.id
        else:
            _hex.hex_asset_id.write(hex_asset_vals)

    @api.model
    def get_json_hex(self):
        """Metodo richiamato dal orm di HexHex.js
            :return: Json del hex."""
        dict_hex = {
            'id': self.id,
            'index': self.index,
            'color': self.color,
            'hex_asset_id': {
                'rotation': self.hex_asset_id.rotation,
                'tile_id': self.hex_asset_id.asset_id.id,
            },
        }
        json_hex = json.dumps(dict_hex)
        return json_hex
