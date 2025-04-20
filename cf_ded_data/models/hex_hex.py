from odoo import models


class HexHex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.hex', 'mixin.import.json']

    @staticmethod
    def get_restrict_domain():
        """OVERRIDE: Da ereditare nei modelli che implementano il mixin."""
        domain = [('status', '=', 'script')]
        return domain
