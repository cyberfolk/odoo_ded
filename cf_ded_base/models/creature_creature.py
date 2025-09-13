from odoo import fields, models, api
from ..utility.exp import MAP_CR_EXP


class CreatureCreature(models.Model):
    _name = "creature.creature"
    _description = "Creatura"

    _sql_constraints = [
        ('unique_creature_base_mixin_name', 'UNIQUE(name)', 'Il nome deve essere univoco!')
    ]

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
        required=True,
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Creatura",
    )

    image = fields.Image(
        string="Immagine",
    )

    link_5et = fields.Char(
        string="Link 5et",
        help="Link al form della creatura su 5etools per avere maggiori dettagli."
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura di riferimento",
    )

    is_legendary = fields.Boolean(
        string="Mostro Leggendario",
        help="Se vero, la creatura è un Mostro Leggendario.",
    )

    is_npc = fields.Boolean(
        string="NPC",
        help="Se vero, la creatura è un NPC.",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NPC DESCRIPTIVE ------------------------------------------------------------------------------------
    titles = fields.Char(
        string="Titoli",
    )
    motivation = fields.Text(
        string="Motivazione",
    )
    needs = fields.Text(
        string="Bisogni"
    )
    offers = fields.Text(
        string="Offre"
    )
    appearance = fields.Text(
        string="Aspetto",
    )
    social_role = fields.Text(
        string="Ruolo Sociale",
    )
    pc_relation = fields.Text(
        string="Ruolo verso i PG",
        help="Se può essere d'aiuto, minaccia, o altro verso i PG.",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - CR EXP -------------------------------------------------------------------------------------------
    cr = fields.Float(
        string="Grado Sfida",
        required=True,
    )
    exp = fields.Float(
        string="Exp",
        compute="_compute_exp",
        help="Esperienza ottenuta eliminando la creatura."
    )

    @api.depends("cr")
    def _compute_exp(self):
        for record in self:
            record.exp = MAP_CR_EXP[str(record.cr)]

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NOT USED -----------------------------------------------------------------------------------------
    ac = fields.Integer(string="Classe Armatura")
    hp = fields.Integer(string="Punti Vita")
    hd = fields.Char(string="Dadi Vita")
    speed = fields.Integer(string="Velocita' m/r")
    wisdom = fields.Integer(string="Saggezza")
    strength = fields.Integer(string="Forza")
    charisma = fields.Integer(string="Carisma")
    dexterity = fields.Integer(string="Destrezza")
    constitution = fields.Integer(string="Costituzione")
    intelligence = fields.Integer(string="Intelligenza")
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - TYPE TAG -----------------------------------------------------------------------------------------
    is_skip = fields.Boolean(
        string="Sconosciuta",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è sconosciuta dalla maggior parte dei DM. Considera creature più note.",
        store=True
    )

    is_cool = fields.Boolean(
        string="Interessante",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è molto interessante, e funziona bene per creare atmosfera.",
        store=True
    )

    is_endemic = fields.Boolean(
        string="Endemico",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è una specie endemica del bioma, ed è aggressiva.",
        store=True
    )

    is_boss = fields.Boolean(
        string="Boss",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è un boss di fine Quest.",
        store=True
    )

    is_not_violent = fields.Boolean(
        string="Non violento",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è non violenta, potrebbe sapere combattere, ma non attaccherebbe per prima.",
        store=True
    )

    is_innocuous = fields.Boolean(
        string="Innocuo",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura è innocua, anche se attacca non sarebbe una minaccia.",
        store=True
    )

    is_social = fields.Boolean(
        string="Sociale",
        compute="_compute_boolean_tag",
        help="Se vero, la creatura fa parte di una struttura sociale organizzata.",
        store=True
    )

    tag_ids = fields.Many2many(
        comodel_name="creature.tag",
        string="Tag",
        help="Tag della creatura"
    )

    type_id = fields.Many2one(
        comodel_name="creature.type",
        string="Tipo",
        help="Tipo di creatura"
    )

    @api.depends("tag_ids")
    def _compute_boolean_tag(self):
        for record in self:
            record.is_boss = True if "Boss" in record.tag_ids.mapped("name") else False
            record.is_skip = True if "Sconosciuto" in record.tag_ids.mapped("name") else False
            record.is_cool = True if "Interessante" in record.tag_ids.mapped("name") else False
            record.is_social = True if "Sociale" in record.tag_ids.mapped("name") else False
            record.is_endemic = True if "Endemico" in record.tag_ids.mapped("name") else False
            record.is_innocuous = True if "Innocuo" in record.tag_ids.mapped("name") else False
            record.is_not_violent = True if "Non Violento" in record.tag_ids.mapped("name") else False

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - BIOME --------------------------------------------------------------------------------------------
    biome_high_prob_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_biome_high_prob_rel",  # Specify a unique relation name
        string="Biomi %Alta",
        help="Biomi con Alta probabilità di trovare la creatura."
    )
    biome_low_prob_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_biome_low_prob_rel",  # Specify a unique relation name
        string="Biomi %Bassa",
        help="Biomi con Bassa probabilità di trovare la creatura."
    )
    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        string="Biomi",
        compute="_compute_biome_ids",
        help="Lista che comprende Biomi %Bassa e Biomi %Alta.",
        store=True
    )

    @api.depends("biome_high_prob_ids", "biome_low_prob_ids")
    def _compute_biome_ids(self):
        for record in self:
            record.biome_ids = record.biome_high_prob_ids + record.biome_low_prob_ids

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ----------------------------------------------------------------------------------
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="quest_creature_rel",
        # column1="quest_id",
        # column2="creature_id",
    )
    poi_ids = fields.Many2many(
        string="Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_creature_rel",
        # column1="poi_id",
        # column2="creature_id",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="faction_creature_rel",
        # column1="creature_id",
        # column2="faction_id",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="creature_creature_rel",
        column1="creature1_id",
        column2="creature2_id",
    )
    # endregion --------------------------------------------------------------------------------------------------------
