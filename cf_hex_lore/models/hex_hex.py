from odoo import fields, models, api


class HexHex(models.Model):
    _inherit = "hex.hex"

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

    description = fields.Html(
        string="Descrizione",
    )

    image = fields.Image(
        string="Immagine",
    )

    npc_ids = fields.Many2many(
        comodel_name="creature.npc",
        relation="creature_npc_hex_script_rel",
        string="NPCs",
        help="Elenco NPC che si posso trovare in questo Esagono Scriptato."
    )

    faction_ids = fields.Many2many(
        comodel_name="creature.faction",
        relation="creature_faction_hex_script_rel",
        string="Fazioni",
        help="Elenco Fazioni che si posso trovare in questo Esagono Scriptato."
    )

    structure_id = fields.Many2one(
        comodel_name="structure.structure",
        string="Struttura Principale",
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura Principale",
    )

    image_gallery_ids = fields.Many2many(
        'ir.attachment',
        string="Altre Immagini",
        domain=[('mimetype', 'ilike', 'image')],
        help="Upload multiple images"
    )

    wild_encounter_ids = fields.Many2many(
        comodel_name="creature.encounter",
        relation="creature_encounter_hex_script_rel",
        string="Scontri Selvaggi",
        help="Scontri Selvaggi che si possono verificare nell'Esagono Scriptato.",
    )

    encounter_encounter_ids = fields.One2many(
        comodel_name="encounter.encounter",
        inverse_name="hex_id",
        string="Incontri Casuali",
        help="Incontri Casuali che si possono verificare nell'Esagono Scriptato.",
    )
