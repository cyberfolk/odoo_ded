from odoo import models


class CreatureTag(models.Model):
    _name = "creature.tag"
    _inherit = ['creature.tag', 'mixin.import.py']

    def from_rec_to_dikt(self, rec):
        """Da ereditare nei modelli che implementano il mixin."""

        dikt = {
            'name': rec.name,
            'is_faction': rec.is_faction,
        }

        return dikt
