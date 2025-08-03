import logging

from odoo import models

_logger = logging.getLogger(__name__)


class HexHex(models.Model):
    _inherit = "hex.hex"

    def export_json_for_gpt(self):
        """OVERRIDE: Escludo campi che non servono per comunicare con GPT."""

        skip_fields = [
            "type",
            "index",
            "quad_id",
            "border_N",
            "border_NE",
            "border_SE",
            "border_S",
            "border_SW",
            "border_NW",
            "status",
            "row",
            "col",
            "image",
            "image_gallery_ids",
            "wild_encounter_ids",
            "encounter_encounter_ids",
            "hex_asset_id",
        ]

        return {
            'type': 'ir.actions.act_url',
            'url': f"/data_handler/export_json?model={self._name}&ids={self.ids}&skip_fields={skip_fields}",
            'target': 'new',
        }
