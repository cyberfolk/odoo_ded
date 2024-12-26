from odoo import models


class CreatureTag(models.Model):
    _name = "creature.tag"
    _inherit = ['creature.tag', 'mixin.import.json']

    # @staticmethod
    # def from_rec_to_dikt(rec):
    #     """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
    #
    #     dikt = {
    #         'name': rec.name,
    #         'is_faction': rec.is_faction,
    #     }
    #
    #     return dikt

# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'creature_ids': ('many2many', 'creature.creature'),
#     'is_faction':   ('boolean', None),
#     'name':         ('char', None),
# }
