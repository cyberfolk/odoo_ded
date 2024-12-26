import base64
import logging
from pathlib import Path

from odoo import models, api

_logger = logging.getLogger(__name__)


class AssetTile(models.Model):
    _inherit = "asset.tile"
    _description = "Asset Tile"

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
