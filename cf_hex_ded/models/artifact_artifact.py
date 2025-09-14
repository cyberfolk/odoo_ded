from odoo import fields, models, api, Command


class ArtifactArtifact(models.Model):
    _inherit = "artifact.artifact"

    hex_ids = fields.Many2many(
        comodel_name="hex.hex",
        relation="artifact_hex_rel",
        string="HEXs",
    )
