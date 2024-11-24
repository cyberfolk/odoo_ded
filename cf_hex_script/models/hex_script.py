import json
from odoo import api, fields, models, Command, api


class HexScript(models.Model):
    _name = "hex.script"
    _description = "Script Cell"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Hex-Script"
    )

    biome_id = fields.Many2one(
        comodel_name='biome.biome',
        string="Biome",
        help="Bioma contenuto in questo Hex-Script"
    )

    sml = fields.Integer(
        string="SML",
        help="Difficoltà Hex-Script. Calcolata come 'Scontro Mortale per 4 PG di Livello SML'"
    )

    hex_id = fields.Many2one(
        comodel_name='hex.hex',
        compute='compute_hex',
        inverse='hex_inverse',
        string="Esagono",
    )

    hex_ids = fields.One2many(
        comodel_name='hex.hex',
        inverse_name='hex_script_id'
    )

    @api.depends('hex_ids')
    def compute_hex(self):
        if len(self.hex_ids) > 0:
            self.hex_id = self.hex_ids[0]

    def hex_inverse(self):
        if len(self.hex_ids) > 0: # delete previous reference
            hex = self.env['hex.hex'].browse(self.hex_ids[0].id)
            hex.hex_id = False
        self.hex_id.hex_script_id = self  # set new reference
