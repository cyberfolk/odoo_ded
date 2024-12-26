from odoo import models


class HexHex(models.Model):
    _name = "hex.hex"
    _inherit = ['hex.hex', 'mixin.import.json']
