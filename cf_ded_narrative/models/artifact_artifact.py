from odoo import fields, models


class ArtifactArtifact(models.Model):
    _inherit = ['artifact.artifact', 'narrative.relation.mixin']
    _name = 'artifact.artifact'
