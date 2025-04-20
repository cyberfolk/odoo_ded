import base64
import json
import logging
from pathlib import Path

from odoo import models, api

_logger = logging.getLogger(__name__)


class AssetTile(models.Model):
    _name = "asset.tile"
    _description = "Asset Tile"

    name = fields.Char(string="Nome", required=True)
    image = fields.Image(string="Image", attachment=True)  # Usa attachment=True per il filestore
    sub_dir = fields.Char(string="Subdir", default="")
    hex_ids = fields.Many2many(comodel_name="hex.hex", string="Hexagons")

    @api.model
    def get_json_tiles_kit(self):
        """Metodo richiamato dal orm di view_map.js
            :return: Json del TilesKit."""
        asset_tiles = list(self.env['asset.tile'].search([]))
        asset_tiles_dikt = [{'name': x.name, 'sub_dir': x.sub_dir, 'id': x.id} for x in asset_tiles]
        tiles_kit = {}
        name = ''
        for tile in asset_tiles_dikt:
            sub_dirs = tile.pop('sub_dir').split('/')
            current_level = tiles_kit

            # Itera su tutte le sottodirectory per creare la struttura annidata
            for sub_dir in sub_dirs:
                if sub_dir not in current_level:
                    current_level[sub_dir] = {}
                current_level = current_level[sub_dir]

            # Aggiungi il tile all'ultimo livello
            if 'tiles' not in current_level:
                current_level['tiles'] = []
            current_level['tiles'].append(tile)
            current_level['name'] = ' > '.join(sub_dirs)

        json_tiles_kit = json.dumps(tiles_kit)
        return json_tiles_kit

    @api.model
    def load_images(self):
        _logger.info(f"START load_images ({self._name})")
        # Percorso della cartella con le immagini
        file_path = Path(__file__).resolve().parents[1] / 'static/asset/tile'

        # Usa Path.rglob per trovare tutti i file PNG nelle sottocartelle
        for img_path in file_path.rglob('*.png'):
            sub_dir = img_path.relative_to(file_path).parent.as_posix()

            # Apri e codifica l'immagine in base64
            with img_path.open('rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data)

                if self.search([('name', '=', img_path.name)]):
                    _logger.warning(f'Il {self._name} {img_path.name} esiste già')
                    continue

                # Crea un record con l'immagine
                self.create({
                    'name': img_path.name,  # Usa il nome del file come nome del record
                    'image': img_base64,
                    'sub_dir': sub_dir,
                })
        _logger.info(f"END   load_images ({self._name})")
