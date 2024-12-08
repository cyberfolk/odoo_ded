from odoo import fields, models, api


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
        help="Difficoltà Hex-Script. Calcolata come 'Scontro Mortale per 4 PG di Livello SML'",
        default=1
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

    description = fields.Html(
        string="Descrizione",
    )

    image_primary = fields.Image(
        string="Immagine",
    )

    @api.depends('hex_ids')
    def compute_hex(self):
        if len(self.hex_ids) > 0:
            self.hex_id = self.hex_ids[0]

    def hex_inverse(self):
        if len(self.hex_ids) > 0:  # delete previous reference
            hex = self.env['hex.hex'].browse(self.hex_ids[0].id)
            hex.hex_id = False
        self.hex_id.hex_script_id = self  # set new reference

    wild_encounter_ids = fields.Many2many(
        comodel_name="creature.encounter",
        relation="creature_encounter_hex_script_rel",
        string="Scontri Selvaggi",
        help="Scontri Selvaggi che si possono verificare nell'Esagono Scriptato.",
    )

    random_encounter_ids = fields.One2many(
        comodel_name="random.encounter",
        inverse_name="hex_script_id",
        string="Incontri Casuali",
        help="Incontri Casuali che si possono verificare nell'Esagono Scriptato.",
    )