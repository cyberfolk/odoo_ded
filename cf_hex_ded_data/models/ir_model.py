import logging

from odoo import models

_logger = logging.getLogger(__name__)
INIT_MODEL = [
    ("biome.biome", 'name', 'creature_high_prob_ids,creature_low_prob_ids,encounter_ids,hex_ids'),
    ("structure.structure", 'name', ''),
    ("creature.tag", 'name', 'creature_ids'),
    ("creature.type", 'name', 'creature_ids'),
    ("creature.creature", 'name', ''),
    ("creature.npc", 'name', ''),
    ("creature.faction", 'name', ''),
    ("creature.encounter", 'name', ''),
    ("creature.encounter.line", 'name', 'encounter_ids'),
    ("hex.hex", 'name', ''),
]


class IrModel(models.Model):
    _inherit = "ir.model"

    def init_data_handler_fields(self):
        for model_name, unique_fields, skip_fields in INIT_MODEL:
            model = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
            model.support_field_fix('x_data_id', 'Data ID')
            model.support_field_fix('x_data_hash', 'Data Hash')
            model.unique_fields_str = unique_fields
            model.skip_fields_str = skip_fields
