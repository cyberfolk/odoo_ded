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

    is_legendary = fields.Boolean(
        string="Mostro Leggendario",
        help="Se vero, la creatura è un Mostro Leggendario.",
    )

    is_npc = fields.Boolean(
        string="NPC",
        help="Se vero, la creatura è un NPC.",
    )

    is_base = fields.Boolean(
        string="Base",
        compute='_compute_is_base',
        store=True,
    )

    @api.depends('is_legendary', 'is_npc')
    def _compute_is_base(self):
        for rec in self:
            rec.is_base = not rec.is_legendary and not rec.is_npc

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NPC DESCRIPTIVE ----------------------------------------------------------------------------------
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

    # region FIELDS - NARRATIVE ENTITY - BASE --------------------------------------------------------------------------
    quest_ids = fields.Many2many(
        string="(Base) Missioni",
        comodel_name="quest.quest",
        relation="quest_creature_rel",
    )
    poi_ids = fields.Many2many(
        string="(Base) Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_creature_rel",
    )
    faction_ids = fields.Many2many(
        string="(Base) Fazioni",
        comodel_name="creature.faction",
        relation="faction_creature_rel",
    )
    creature_ids = fields.Many2many(
        string="(Base) Creature",
        comodel_name="creature.creature",
        relation="creature_creature_rel",
        domain=[('is_base', '=', True)],
        column1="creature1_id",
        column2="creature2_id",
    )
    npc_ids = fields.Many2many(
        string="(Base) NPCs",
        comodel_name="creature.creature",
        relation="creature_npc_rel",
        domain=[('is_npc', '=', True)],
        column1="creature_id",
        column2="npc_ids",
    )
    monster_ids = fields.Many2many(
        string="(Base) Monster",
        comodel_name="creature.creature",
        relation="creature_monster_rel",
        domain=[('is_legendary', '=', True)],
        column1="creature_id",
        column2="monster_id",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY - NPC ---------------------------------------------------------------------------
    quest_npc_ids = fields.Many2many(
        string="(NPC) Missioni",
        comodel_name="quest.quest",
        relation="quest_npc_rel",
    )
    poi_npc_ids = fields.Many2many(
        string="(NPC) Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_npc_rel",
    )
    faction_npc_ids = fields.Many2many(
        string="(NPC) Fazioni",
        comodel_name="creature.faction",
        relation="faction_npc_rel",
    )
    creature_npc_ids = fields.Many2many(
        string="(NPC) Creature",
        comodel_name="creature.creature",
        relation="creature_npc_rel",
        domain=[('is_base', '=', True)],
        column1="creature_id",
        column2="npc_ids",
    )
    npc_npc_ids = fields.Many2many(
        string="(NPC) NPCs",
        comodel_name="creature.creature",
        relation="npc_npc_rel",
        domain=[('is_npc', '=', True)],
        column1="npc1_ids",
        column2="npc2_ids",
    )
    monster_npc_ids = fields.Many2many(
        string="(NPC) Monster",
        comodel_name="creature.creature",
        relation="monster_npc_rel",
        domain=[('is_legendary', '=', True)],
        column1="monster_id",
        column2="npc_id",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY - MONSTER -----------------------------------------------------------------------
    quest_monster_ids = fields.Many2many(
        string="(Monster) Missioni",
        comodel_name="quest.quest",
        relation="quest_monster_rel",
    )
    poi_monster_ids = fields.Many2many(
        string="(Monster) Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_monster_rel",
    )
    faction_monster_ids = fields.Many2many(
        string="(Monster) Fazioni",
        comodel_name="creature.faction",
        relation="faction_monster_rel",
    )
    creature_monster_ids = fields.Many2many(
        string="(Monster) Creature",
        comodel_name="creature.creature",
        relation="creature_monster_rel",
        domain=[('is_base', '=', True)],
        column1="creature_id",
        column2="monster_id",
    )
    npc_monster_ids = fields.Many2many(
        string="(Monster) NPCs",
        comodel_name="creature.creature",
        relation="monster_npc_rel",
        domain=[('is_npc', '=', True)],
        column1="monster_id",
        column2="npc_id",
    )
    monster_monster_ids = fields.Many2many(
        string="(Monster) Monster",
        comodel_name="creature.creature",
        relation="monster_monster_rel",
        domain=[('is_legendary', '=', True)],
        column1="monster1_id",
        column2="monster2_id",
    )

    # endregion --------------------------------------------------------------------------------------------------------

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._sync_creature_links()
        return record

    def write(self, vals):
        res = super().write(vals)
        self._sync_creature_links()
        return res

    def _sync_creature_links(self):
        Creature = self.env['creature.creature']
        all_creatures = Creature.search([])

        mons = all_creatures.filtered(lambda c: c.is_legendary)
        base = all_creatures.filtered(lambda c: c.is_base)
        npcs = all_creatures.filtered(lambda c: c.is_npc)

        for rec in self:
            # 1. Base <-> Base
            _sync_m2m_field(rec.id, set(rec.creature_ids.ids), base, 'creature_ids', rec.is_base)

            # 2. Base <-> NPC
            _sync_m2m_field(rec.id, set(rec.npc_ids.ids), npcs, 'creature_npc_ids', rec.is_base)
            _sync_m2m_field(rec.id, set(rec.creature_npc_ids.ids), base, 'npc_ids', rec.is_npc)

            # 3. Base <-> Monster
            _sync_m2m_field(rec.id, set(rec.monster_ids.ids), mons, 'creature_monster_ids', rec.is_base)
            _sync_m2m_field(rec.id, set(rec.creature_monster_ids.ids), base, 'monster_ids', rec.is_legendary)

            # 4. NPC <-> NPC
            _sync_m2m_field(rec.id, set(rec.npc_npc_ids.ids), npcs, 'npc_npc_ids', rec.is_npc)

            # 5. Monster <-> NPC
            _sync_m2m_field(rec.id, set(rec.npc_monster_ids.ids), npcs, 'monster_npc_ids', rec.is_legendary)
            _sync_m2m_field(rec.id, set(rec.monster_npc_ids.ids), mons, 'npc_monster_ids', rec.is_npc)

            # 6. Monster <-> Monster
            _sync_m2m_field(rec.id, set(rec.monster_monster_ids.ids), mons, 'monster_monster_ids', rec.is_legendary)


def _sync_m2m_field(self_id, source_ids, target_model, reverse_field_name, check):
    """Sincronizza un campo Many2many in modo bidirezionale sullo stesso modello.

    Questa funzione assicura che se A è collegato a B, allora B sia collegato anche ad A
    tramite il campo `reverse_field_name`. Funziona anche per rimuovere i collegamenti
    se vengono recisi da un lato.

    Args:
        check (bool): Se False, non esegue alcuna azione
        self_id (int): L'ID del record principale (quello da cui si parte)
        source_ids (set[int]): Gli ID dei record che il record principale collega (es `creature_ids`, `npc_ids`, etc)
        target_model (recordset): L'elenco dei possibili target da sincronizzare (es tutti i mostri, NPC o creature)
        reverse_field_name (str): Il nome del campo Many2many opposto da sincronizzare
    """
    if not check:
        return

    for target in target_model:
        # Evita il confronto con sé stesso (utile nei collegamenti simmetrici es. npc_npc_ids)
        if target.id == self_id:
            continue

        # Ottiene il campo opposto dal target (es. creature_ids, npc_npc_ids, ecc.)
        reverse_field = getattr(target, reverse_field_name)

        # Se il record principale è collegato al target MA il target NON è collegato a lui → rimuovi
        if self_id in reverse_field.ids and target.id not in source_ids:
            setattr(target, reverse_field_name, [(3, self_id)])

        # Se il record principale è collegato al target MA il target NON è ancora collegato a lui → aggiungi
        elif self_id not in reverse_field.ids and target.id in source_ids:
            setattr(target, reverse_field_name, [(4, self_id)])
