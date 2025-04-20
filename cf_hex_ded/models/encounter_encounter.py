from odoo import fields, models, api


class RandomEncounter(models.Model):
    _inherit = "encounter.encounter"

    hex_id = fields.Many2one(
        comodel_name="hex.hex",
        string="Hex Script",
    )
