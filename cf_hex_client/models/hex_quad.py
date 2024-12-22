import json

from odoo import api, models


class Quadrant(models.Model):
    _inherit = "hex.quad"

    @api.model
    def get_json_quad(self, quad_id):
        """Metodo richiamato dal orm di quad.js
            :param quad_id: Id quadrante.
            :return: Json del quadrante."""

        # Definiamo i campi che ci interessano
        quad_fields = ['id', 'code', 'index', 'row', 'col', 'hex_ids', 'missing_ids', 'type']
        hex_fields = ['id', 'code', 'index', 'row', 'col', 'sml', 'biome_id', 'hex_asset_id']
        hex_asset_fields = ['asset_id', 'rotation']
        biome_fields = ['id', 'color']

        self_quad = self.env['hex.quad'].browse(quad_id)
        quad_dict = self_quad.read(quad_fields)[0]
        quad_dict['hex_ids'] = self_quad.hex_ids.read(hex_fields)
        quad_dict['missing_ids'] = self_quad.missing_ids.read(hex_fields)
        quad_dict['external_hexs'] = [x.read(hex_fields)[0] for x in self_quad.get_external_hexs() if x]

        # Creo la mappa di raccordo per i Biomi
        biomes = self.env['biome.biome'].search([('state', '=', 'active')]).read(biome_fields)
        biomes_map = {x['id']: x['color'] for x in biomes}

        # Creo la mappa di raccordo per gli Asset
        hex_assets = self.env['hex.asset.tile'].search([]).read(hex_asset_fields)
        hex_assets_map = {x['id']: {'tile_id': x['asset_id'][0], 'rotation': x['rotation']} for x in hex_assets}

        # Rifinisco la hex_map con solo i valori da passare al front_end
        for _hex in quad_dict['hex_ids']:
            if hex_asset_id := _hex.get('hex_asset_id'):  # Aggiorna hex_asset_id, se presente
                _hex['hex_asset_id'] = hex_assets_map[hex_asset_id[0]]
            if biome_id := _hex.get('biome_id'):  # Assegna il colore basato su biome_id, se presente
                _hex['color'] = biomes_map[biome_id[0]]
            else:
                _hex['color'] = '#DDDDDD'
            _hex.pop('biome_id', None)

        json_quad = json.dumps(quad_dict)
        return json_quad

    @api.model
    def get_external_hexs(self):
        hex_00_01 = self.hex_ids.filtered(lambda x: x.index == 1)
        hex_02_01 = hex_00_01.border_N.border_N
        hex_02_03 = hex_02_01.border_SE.border_SE
        hex_02_05 = hex_02_03.border_S.border_S
        hex_02_07 = hex_02_05.border_SW.border_SW
        hex_02_09 = hex_02_07.border_NW.border_NW
        hex_02_11 = hex_02_09.border_N.border_N
        hex_list = [
            hex_02_01.border_NW, hex_02_01.border_N, hex_02_01.border_NE,
            hex_02_03.border_N, hex_02_03.border_NE, hex_02_03.border_SE,
            hex_02_05.border_NE, hex_02_05.border_SE, hex_02_05.border_S,
            hex_02_07.border_SE, hex_02_07.border_S, hex_02_07.border_SW,
            hex_02_09.border_S, hex_02_09.border_SW, hex_02_09.border_NW,
            hex_02_11.border_SW, hex_02_11.border_NW, hex_02_11.border_N
        ]
        return hex_list
