import logging

from odoo import models
from odoo.addons.cf_data_handler.utilities.utility import EXCLUDED_FIELDS

_logger = logging.getLogger(__name__)


class CreatureFaction(models.Model):
    _inherit = "creature.faction"

    def export_json_for_gpt(self):
        """OVERRIDE: Escludo campi che non servono per comunicare con GPT."""

        skip_fields = [
            "code",
            "state",
            "cosmology",
            "parent_id",
            "creature_ids",
            "encounter_ids",
            "good_evil_axis",
        ]
        custom_transform_method = 'from_rec_to_dikt_for_gp'

        return {
            'type': 'ir.actions.act_url',
            'url': f"/data_handler/export_json?model={self._name}"
                   f"&ids={self.ids}"
                   f"&skip_fields={skip_fields}"
                   f"&custom_transform_method={custom_transform_method}",
            'target': 'new',
        }

    @staticmethod
    def from_rec_to_dikt_for_gp(rec, skip_fields=None):
        """Trasforma un record di Odoo in un dizionario pe GPT."""

        if skip_fields:
            EXCLUDED_FIELDS.update(skip_fields)

        if rec.state not in ['active', 'upcoming']:
            return False

        dikt = {}
        for f_name, f_info in rec._fields.items():  # f_name  -> field_name, f_info -> field_info
            f_value = rec[f_name]  # f_value -> field_value
            f_type = f_info.type  # f_type  -> field_type

            if not f_value:
                continue

            if f_name == 'desc_creature':
                dikt[f_name] = rec.desc_creature
                continue

            if f_name in ['child_ids', 'npc_ids', 'hex_ids']:
                dikt[f_name] = rec.mapped(f'{f_name}.name')
                continue

            if (f_name in EXCLUDED_FIELDS or f_info.compute or f_info.related) and f_name != 'name':
                continue
            elif f_type in ['binary']:
                dikt[f_name] = f_value.decode('utf-8') if f_value else ''
            elif f_type in ['html']:
                dikt['description'] = str(f_value) if f_value else ''
            elif f_type in ['many2one']:
                dikt[f_name] = f_value.get_unique_dict() or False  # TODO f_value.get_inner_dict()
            elif f_type in ['many2many', 'one2many']:
                dikt[f_name] = [x.get_unique_dict() for x in f_value] if f_value else []
            else:
                dikt[f_name] = f_value

        return dikt
