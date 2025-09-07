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

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        relation="creature_hex_script_rel",
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

    completion_percentage = fields.Float(
        string="Completamento",
        compute="_compute_completion_percentage",
        help="Percentuale di campi completati sul totale dei campi modello."
    )

    settlement_id = fields.Many2one(
        comodel_name="settlement.settlement",
        string="Insediamento",
        help="Insediamento presente nell’esagono",
    )

    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="point_of_interest_hex_rel",
    )


    def _compute_completion_percentage(self):
        target_fields = [
            'image', 'creature_ids', 'biome_id', 'faction_ids', 'creature_id', 'description',
            'structure_id', 'image_gallery_ids', 'wild_encounter_ids', 'encounter_encounter_ids',
        ]
        for rec in self:
            filled_fields = sum(1 for field in target_fields if rec[field])

            filled_fields += 1 if rec.name != rec.code else 0  # Controllo aggiuntivo se 'name' è diverso da 'code'

            filled_fields += 1 if rec.sml != 1 else 0  # Controllo aggiuntivo se 'sml' è diverso da 1

            total_fields = len(target_fields) + 2  # +2 per i due controlli aggiuntivi
            rec.completion_percentage = (filled_fields / total_fields) * 100 if total_fields else 0
