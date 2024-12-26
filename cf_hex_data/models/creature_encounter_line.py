from odoo import models


class CreatureEncounterLine(models.Model):
    _name = "creature.encounter.line"
    _inherit = ['creature.encounter.line', 'mixin.import.json']
