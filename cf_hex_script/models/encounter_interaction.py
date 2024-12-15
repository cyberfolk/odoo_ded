from odoo import fields, models, api


class RandomEncounter(models.Model):
    _inherit = "encounter.interaction"
    _description = "Random Encounter"

    hex_script_id = fields.Many2one(
        comodel_name="hex.script",
        string="Hex Script",
    )
