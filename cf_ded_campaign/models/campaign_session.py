from odoo import fields, models, api
from ...cf_ded_base.utility.exp import get_level_by_exp, get_exp_bar, get_budget_exp


class CampaignSession(models.Model):
    _name = "campaign.session"
    _description = "Sessione"

    name = fields.Char(
        string="Nome",
    )
    state = fields.Selection(
        string="Stato",
        selection=[("draft", "Bozza"), ("confirmed", "Confermata")],
        default="draft",
    )
    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Campagna",
    )

    image = fields.Image(
        string="Immagine",
    )

    master_id = fields.Many2one(
        comodel_name="res.partner",
        string="Master",
        domain="[('rpg_type', '=', 'master')]",
    )

    player_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Players",
        compute="_compute_player_ids",
    )

    date = fields.Date(
        string="Data",
        help="Data della sessione",
        default=fields.Date.context_today,
    )

    campaign_id = fields.Many2one(
        comodel_name="campaign.campaign",
        string="Campagna",
    )

    pg_ids = fields.Many2many(
        comodel_name="campaign.pg",
        string="PG",
        compute="_compute_pg_ids",
    )

    session_pg_ids = fields.One2many(
        comodel_name="campaign.session.pg",
        inverse_name="session_id",
        string="Righe d'appoggio per il computo dell'exp dei PG",
    )
    exp_soglia = fields.Integer(
        string="Exp Soglia",
        compute="_compute_exp_soglia",
        help="Corrisponde alla Media dell'Exp di fine sessione. Ogni PG con Exp sotto alla soglia, viene immediatamente"
             "parificato al valore di soglia."
    )
    exp_gained_common = fields.Integer(
        string="Tot Exp Comune",
        compute="_compute_exp_gained_common",
    )
    # ------------------------------------------------------------------------------------------------------------------
    n_hex_crossed = fields.Integer(
        string="Esagoni attraversati",
    )

    n_hex_crossed_exp = fields.Integer(
        string="Esagoni attraversati: Exp",
        help="Esperienza derivante dal numero di esagoni attraversati per il livello medio del party",
        compute="_compute_n_hex_crossed_exp"
    )
    # ------------------------------------------------------------------------------------------------------------------
    treasure_info_description = fields.Char(
        string="Oro e Info: Descrizione",
        help="Descrizione Oro e Info",
    )

    treasure_info_difficulty = fields.Float(
        string="Oro e Info: Difficoltà",
        help="Difficoltà Oro e Info, per calcolare l'esperienza guadagnata",
    )

    treasure_info_exp = fields.Integer(
        string="Oro e Info: Exp",
        help="Esperienza derivante dal difficoltà di 'Oro e Info' per il livello medio del party",
        compute="_compute_treasure_info_exp"
    )
    # ------------------------------------------------------------------------------------------------------------------
    mission_id = fields.Many2one(
        comodel_name="campaign.mission",
        string="Missione",
    )

    mission_id_difficulty = fields.Float(
        string="Missione: Difficoltà",
        help="Difficoltà Missione, per calcolare l'esperienza guadagnata",
    )

    mission_id_exp = fields.Integer(
        string="Missione: Exp",
        help="Esperienza derivante dal difficoltà Missione per il livello medio del party",
        compute="_compute_mission_id_exp"
    )
    # ------------------------------------------------------------------------------------------------------------------
    encounter_ids = fields.Many2many(
        comodel_name="creature.encounter",
        string="Scontri",
    )

    encounter_exp = fields.Integer(
        string="Scontri: Exp",
        compute="_compute_encounter_exp",
        help="Esperienza derivante dagli scontri.",
    )
    encounter_exp_adj = fields.Integer(
        string="Scontri: Exp Adj",
        compute="_compute_encounter_exp_adj",
        help="Esperienza Aggiustata. Uguale Esperienza Scontri diviso 2.",
    )
    encounter_exp_split = fields.Integer(
        string="Scontri: Exp Adj Divisa",
        compute="_compute_encounter_exp_split",
        help="Esperienza derivante dagli scontri Aggiustata e divisa tra il numero di player nel party.",
    )
    # ------------------------------------------------------------------------------------------------------------------
    party_avg_exp = fields.Integer(
        string="Party Exp Media",
        help="Esperienza Media del Party a inizio sessione.",
        compute="_compute_party_avg_exp"
    )

    party_avg_level = fields.Integer(
        string="Party Livello Medio",
        help="Livello relativo alla media dell'esperienza dei componenti del party.",
        compute="_compute_party_avg_level"
    )
    party_exp_bar = fields.Integer(
        string="Party Barra Exp",
        help="Barra dell'Esperienza per passare al livello successivo, relativa al livello medio del Party.",
        compute="_compute_party_exp_bar",
        store=True
    )

    # ------------------------------------------------------------------------------------------------------------------
    encounter_easy_exp = fields.Integer(
        string="Scontro Facile: Exp",
        compute="_compute_budget_exp"
    )
    encounter_medium_exp = fields.Integer(
        string="Scontro Medio: Exp",
        compute="_compute_budget_exp"
    )
    encounter_hard_exp = fields.Integer(
        string="Scontro Difficile: Exp",
        compute="_compute_budget_exp"
    )
    encounter_deadly_exp = fields.Integer(
        string="Scontro Mortale: Exp",
        compute="_compute_budget_exp"
    )
    daily_budget_exp = fields.Integer(
        string="Daily Budget: Exp",
        compute="_compute_budget_exp",
        help="Daily Budget, Stima dell'esperienza che un party può guadagnare in un giorno senza morire,"
             " riposando adeguatamente tra i vari scontri."
    )
    encounter_easy_exp_percentage = fields.Float(
        string="Scontro Facile: Exp Percentage",
        compute="_compute_budget_exp",
        digits=(16, 2)
    )
    encounter_medium_exp_percentage = fields.Float(
        string="Scontro Medio: Exp Percentage",
        compute="_compute_budget_exp",
        digits=(16, 2)
    )
    encounter_hard_exp_percentage = fields.Float(
        string="Scontro Difficile: Exp Percentage",
        compute="_compute_budget_exp",
        digits=(16, 2)
    )
    encounter_deadly_exp_percentage = fields.Float(
        string="Scontro Mortale: Exp Percentage",
        compute="_compute_budget_exp",
        digits=(16, 2)
    )
    daily_budget_exp_percentage = fields.Float(
        string="Daily Budget: Exp Percentage",
        compute="_compute_budget_exp",
        digits=(16, 2),
    )

    # ------------------------------------------------------------------------------------------------------------------

    @api.onchange('campaign_id')
    def _onchange_campaign_id(self):
        if self.campaign_id and not self.master_id:
            if self.campaign_id.master_id:
                self.master_id = self.campaign_id.master_id

    @api.depends('session_pg_ids')
    def _compute_party_avg_exp(self):
        for rec in self:
            rec.party_avg_exp = sum([pg.exp_start for pg in rec.session_pg_ids]) / (len(rec.session_pg_ids) or 1) or 0

    @api.depends('party_avg_exp')
    def _compute_party_avg_level(self):
        for rec in self:
            rec.party_avg_level = get_level_by_exp(rec.party_avg_exp)

    @api.depends('party_exp_bar', 'treasure_info_difficulty')
    def _compute_treasure_info_exp(self):
        for rec in self:
            rec.treasure_info_exp = rec.treasure_info_difficulty * rec.party_exp_bar

    @api.depends('party_exp_bar', 'mission_id_difficulty')
    def _compute_mission_id_exp(self):
        for rec in self:
            rec.mission_id_exp = rec.mission_id_difficulty * rec.party_exp_bar

    @api.depends('party_exp_bar', 'n_hex_crossed')
    def _compute_n_hex_crossed_exp(self):
        for rec in self:
            rec.n_hex_crossed_exp = rec.n_hex_crossed * 0.05 * rec.party_exp_bar

    @api.depends('party_avg_level')
    def _compute_party_exp_bar(self):
        for rec in self:
            rec.party_exp_bar = get_exp_bar(rec.party_avg_level)

    @api.depends('session_pg_ids')
    def _compute_pg_ids(self):
        for rec in self:
            rec.pg_ids = rec.session_pg_ids.pg_id

    @api.depends('pg_ids')
    def _compute_player_ids(self):
        for rec in self:
            rec.player_ids = rec.pg_ids.player_id

    @api.depends('encounter_ids')
    def _compute_encounter_exp(self):
        for rec in self:
            rec.encounter_exp = sum(enc.exp_adj for enc in rec.encounter_ids)

    @api.depends('encounter_exp')
    def _compute_encounter_exp_adj(self):
        for rec in self:
            rec.encounter_exp_adj = rec.encounter_exp / 2

    @api.depends('encounter_exp_adj', 'player_ids')
    def _compute_encounter_exp_split(self):
        for rec in self:
            rec.encounter_exp_split = rec.encounter_exp_adj / len(rec.session_pg_ids) if rec.player_ids else 0

    @api.depends('session_pg_ids')
    def _compute_budget_exp(self):
        for rec in self:
            liv_start_list = [x.liv_start for x in rec.session_pg_ids]
            easy, medium, hard, deadly, budget = get_budget_exp(liv_start_list)
            rec.encounter_easy_exp = easy
            rec.encounter_medium_exp = medium
            rec.encounter_hard_exp = hard
            rec.encounter_deadly_exp = deadly
            rec.daily_budget_exp = budget
            K = 1 / 2 / len(rec.session_pg_ids) / rec.party_exp_bar if rec.session_pg_ids and rec.party_exp_bar else 0
            rec.encounter_easy_exp_percentage = easy * K
            rec.encounter_medium_exp_percentage = medium * K
            rec.encounter_hard_exp_percentage = hard * K
            rec.encounter_deadly_exp_percentage = deadly * K
            rec.daily_budget_exp_percentage = budget * K

    @api.depends('session_pg_ids')
    def _compute_exp_soglia(self):
        for rec in self:
            exp_end_list = [x.exp_end for x in rec.session_pg_ids] or [0]
            rec.exp_soglia = sum(exp_end_list) / len(exp_end_list or 0)

    @api.depends('mission_id_exp', 'encounter_exp_split', 'n_hex_crossed_exp', 'treasure_info_exp')
    def _compute_exp_gained_common(self):
        for rec in self:
            rec.exp_gained_common = rec.mission_id_exp + rec.encounter_exp_split + rec.n_hex_crossed_exp + rec.treasure_info_exp

    def action_confirm(self):
        self.ensure_one()
        self.state = 'confirmed'
        for session_pg in self.session_pg_ids:
            session_pg.pg_id.exp += (session_pg.exp_end_adj - session_pg.exp_start)

    def action_return_to_draft(self):
        self.ensure_one()
        self.state = 'draft'
        for session_pg in self.session_pg_ids:
            session_pg.pg_id.exp -= (session_pg.exp_end_adj - session_pg.exp_start)

