from odoo import fields, models, api
from ...cf_hex_biome.utility.exp import get_level_by_exp, get_exp_bar, get_budget_exp


class CampaignSession(models.Model):
    _name = "campaign.session"
    _description = "Sessione"

    name = fields.Char(
        string="Nome",
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

    pg_exp_line_ids = fields.One2many(
        comodel_name="campaign.session.pg.exp",
        inverse_name="session_id",
        string="Righe d'appoggio per il computo dell'exp dei PG",
    )
    exp_soglia = fields.Integer(
        string="Exp Soglia",
        compute="_compute_exp_soglia",
        help="Corrisponde alla Media dell'Exp di fine sessione. Ogni PG con Exp sotto alla soglia, viene immediatamente"
             "parificato al valore di soglia."
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
    treasure_and_info_description = fields.Char(
        string="Oro e Info: Descrizione",
        help="Descrizione Oro e Info",
    )

    treasure_and_info_difficulty = fields.Float(
        string="Oro e Info: Difficoltà",
        help="Difficoltà Oro e Info, per calcolare l'esperienza guadagnata",
    )

    treasure_and_info_exp = fields.Integer(
        string="Oro e Info: Exp",
        help="Esperienza derivante dal difficoltà di 'Oro e Info' per il livello medio del party",
        compute="_compute_treasure_and_info_exp"
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

    encounter_ids_exp = fields.Integer(
        string="Scontri: Exp",
        compute="_compute_encounter_ids_exp",
        help="Esperienza derivante dagli scontri.",
    )
    encounter_ids_exp_adj = fields.Integer(
        string="Scontri: Exp Adj",
        compute="_compute_encounter_ids_exp_adj",
        help="Esperienza derivante dagli scontri diviso 2.",
    )
    # ------------------------------------------------------------------------------------------------------------------
    party_avg_exp = fields.Integer(
        string="Party Exp Media",
        help="Esperienza Media del Party, calcolata come la media di tutte le esperienze dei componenti del party",
        compute="_compute_party_avg_exp"
    )

    party_avg_level = fields.Integer(
        string="Party Livello Medio",
        help="Livello relativo alla media dell'esperienza dei componenti del party.",
        compute="_compute_party_avg_level"
    )
    party_avg_exp_bar = fields.Integer(
        string="Party Barra Exp",
        help="Barra dell'Esperienza per passare al livello successivo, relativa al livello medio del Party.",
        compute="_compute_party_avg_exp_bar"
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

    # ------------------------------------------------------------------------------------------------------------------

    @api.onchange('campaign_id')
    def _onchange_campaign_id(self):
        if self.campaign_id and not self.master_id:
            if self.campaign_id.master_id:
                self.master_id = self.campaign_id.master_id

    @api.depends('pg_ids')
    def _compute_party_avg_exp(self):
        for rec in self:
            rec.party_avg_exp = sum(pg.exp for pg in rec.pg_ids) / (len(rec.pg_ids) or 1) or 0

    @api.depends('party_avg_exp')
    def _compute_party_avg_level(self):
        for rec in self:
            rec.party_avg_level = get_level_by_exp(rec.party_avg_exp)

    @api.depends('party_avg_exp_bar', 'treasure_and_info_difficulty')
    def _compute_treasure_and_info_exp(self):
        for rec in self:
            rec.treasure_and_info_exp = rec.treasure_and_info_difficulty * rec.party_avg_exp_bar

    @api.depends('party_avg_exp_bar', 'mission_id_difficulty')
    def _compute_mission_id_exp(self):
        for rec in self:
            rec.mission_id_exp = rec.mission_id_difficulty * rec.party_avg_exp_bar

    @api.depends('party_avg_exp_bar', 'n_hex_crossed')
    def _compute_n_hex_crossed_exp(self):
        for rec in self:
            rec.n_hex_crossed_exp = rec.n_hex_crossed * 0.05 * rec.party_avg_exp_bar

    @api.depends('party_avg_level')
    def _compute_party_avg_exp_bar(self):
        for rec in self:
            rec.party_avg_exp_bar = get_exp_bar(rec.party_avg_level)

    @api.depends('pg_exp_line_ids')
    def _compute_pg_ids(self):
        for rec in self:
            rec.pg_ids = rec.pg_exp_line_ids.pg_id

    @api.depends('pg_ids')
    def _compute_player_ids(self):
        for rec in self:
            rec.player_ids = rec.pg_ids.player_id

    @api.depends('encounter_ids')
    def _compute_encounter_ids_exp(self):
        for rec in self:
            rec.encounter_ids_exp = sum(enc.exp_adj for enc in rec.encounter_ids)

    @api.depends('encounter_ids_exp')
    def _compute_encounter_ids_exp_adj(self):
        for rec in self:
            rec.encounter_ids_exp_adj = rec.encounter_ids_exp / 2

    @api.depends('pg_exp_line_ids')
    def _compute_budget_exp(self):
        for rec in self:
            liv_start_list = [x.liv_start for x in rec.pg_exp_line_ids]
            easy, medium, hard, deadly, budget = get_budget_exp(liv_start_list)
            rec.encounter_easy_exp = easy
            rec.encounter_medium_exp = medium
            rec.encounter_hard_exp = hard
            rec.encounter_deadly_exp = deadly
            rec.daily_budget_exp = budget

    @api.depends('pg_exp_line_ids')
    def _compute_exp_soglia(self):
        for rec in self:
            exp_end_list = [x.exp_end for x in rec.pg_exp_line_ids]
            rec.exp_soglia = sum(exp_end_list) / len(exp_end_list or 0)

