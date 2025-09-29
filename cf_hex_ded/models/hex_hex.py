from odoo import fields, models, api


class HexHex(models.Model):
    _inherit = "hex.hex"

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    biome_id = fields.Many2one(
        comodel_name='biome.biome',
        string="Biome",
        help="Bioma contenuto in questo Hex"
    )

    sml = fields.Integer(
        string="SML",
        help="Difficoltà Hex. Calcolata come 'Scontro Mortale per 4 PG di Livello SML'",
        default=1,
        required=True,
    )

    description = fields.Html(
        string="Descrizione",
    )

    image = fields.Image(
        string="Immagine",
    )

    poi_id = fields.Many2one(
        comodel_name="point.of.interest",
        string="Punto d'Interesse",
    )

    monster_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Mostro Leggendario",
        domain=[('is_legendary', '=', True)]
    )

    image_gallery_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string="Altre Immagini",
        domain=[('mimetype', 'ilike', 'image')],
        help="Upload multiple images"
    )

    wild_encounter_ids = fields.Many2many(
        comodel_name="creature.encounter",
        relation="creature_encounter_hex_script_rel",
        string="Scontri Selvaggi",
        help="Scontri Selvaggi che si possono verificare nel Hex.",
    )

    encounter_encounter_ids = fields.One2many(
        comodel_name="encounter.encounter",
        inverse_name="hex_id",
        string="Incontri Casuali",
        help="Incontri Casuali che si possono verificare nel Hex.",
    )

    completion_percentage = fields.Float(
        string="Completamento",
        compute="_compute_completion_percentage",
        help="Percentuale di campi completati sul totale dei campi modello."
    )

    def _compute_completion_percentage(self):
        target_fields = [
            'biome_id', 'sml', 'description', 'image', 'poi_id', 'image_gallery_ids', 'wild_encounter_ids',
            'encounter_encounter_ids', 'artifact_ids', 'faction_ids', 'lore_item_ids', 'poi_ids', 'quest_ids',
            'settlement_ids', 'creature_ids', 'npc_ids', 'monster_ids',
        ]
        for rec in self:
            filled_fields = sum(1 for field in target_fields if rec[field])

            filled_fields += 1 if rec.name != rec.code else 0  # Controllo aggiuntivo se 'name' è diverso da 'code'

            filled_fields += 1 if rec.sml != 1 else 0  # Controllo aggiuntivo se 'sml' è diverso da 1

            total_fields = len(target_fields) + 2  # +2 per i due controlli aggiuntivi
            rec.completion_percentage = (filled_fields / total_fields) * 100 if total_fields else 0

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    artifact_ids = fields.Many2many(
        comodel_name="artifact.artifact",
        relation="artifact_hex_rel",
        string="Artefatti",
    )
    faction_ids = fields.Many2many(
        comodel_name="creature.faction",
        relation="faction_hex_rel",
        string="Fazioni",
    )
    lore_item_ids = fields.Many2many(
        comodel_name="lore.item",
        relation="lore_item_hex_rel",
        string="Lore Items",
    )
    poi_ids = fields.Many2many(
        comodel_name="point.of.interest",
        relation="poi_hex_rel",
        string="Punti d'Interesse",
    )
    quest_ids = fields.Many2many(
        comodel_name="quest.quest",
        relation="quest_hex_rel",
        string="Missioni",
    )
    settlement_ids = fields.Many2many(
        comodel_name="settlement.settlement",
        relation="settlement_hex_rel",
        string="Insediamenti",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="hex_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="hex_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="hex_monster_rel",
        domain=[('is_legendary', '=', True)]
    )

    # endregion --------------------------------------------------------------------------------------------------------

    # region NOMENCLATURA ESAGONI --------------------------------------------------------------------------------------
    code_complete = fields.Char(
        string="Codice Completo",
        compute="_compute_alias_and_slug_and_title",
        store=True,
        help="[Hex Code]-[BIO]-SML[X]"
    )

    code_complete_human = fields.Char(
        string="Codice Completo (leggibile)",
        compute="_compute_alias_and_slug_and_title",
        store=True,
        help="[Hex Code] — [Bioma nome] (SML[X])"
    )

    @api.depends('map_id.name', 'quad_id.code', 'code', 'sml', 'biome_id.code')
    def _compute_alias_and_slug_and_title(self):
        for rec in self:
            sml = rec.sml or 'x'
            biome_code = rec.biome_id.code or 'biome_code'
            biome_name = rec.biome_id.name or 'biome_name'
            hex_code = rec.code or 'hex_code'

            if rec.type == 'v1_19_q':
                ma = rec.map_id.index_19q or 'NAN'
                hex_code = f"{ma}.{hex_code}"

            rec.code_complete = f"{hex_code}.{biome_code}.SML{sml}"
            rec.code_complete_human = f"{hex_code} — {biome_name} (SML {sml})"
# endregion --------------------------------------------------------------------------------------------------------
