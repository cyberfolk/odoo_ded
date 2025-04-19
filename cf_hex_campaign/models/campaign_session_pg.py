from odoo import fields, models, api
from ...cf_hex_biome.utility.exp import get_level_by_exp, get_exp_bar, get_exp_next_level


class CampaignSessionPg(models.Model):
    _name = "campaign.session.pg"
    _description = "Righe d'appoggio per il computo dell'exp dei PG"

    session_id = fields.Many2one(
        comodel_name="campaign.session",
        string="Sessione",
    )
    pg_id = fields.Many2one(
        comodel_name="campaign.pg",
        string="PG",
    )
    player_id = fields.Many2one(
        comodel_name="res.partner",
        related="pg_id.player_id",
        string="Player",
    )
    exp_start = fields.Integer(
        string="Exp Start",
        help="Exp di questo PG a inizio sessione."
    )
    liv_start = fields.Integer(
        string="Livello Start",
        compute="_compute_liv_start",
        help="Livello di questo PG a inizio sessione."
    )
    exp_bar = fields.Integer(
        string="Barra Exp",
        compute="_compute_exp_bar",
        help="Barra d'esperienza di questo PG."
    )
    exp_next_level = fields.Integer(
        string="Exp prossimo livello",
        compute="_compute_exp_next_level",
        help="Exp da raggiungere per salire di livello."
    )
    exp_gained_single = fields.Integer(
        string="Exp Guadagnata Singola",
        compute="_compute_exp_gained_single",
        help="Esperienza che il player ha guadagnata in questa sessione Singolarmente. "
             "Comprende: Ruolo, RP, Aiuto."
    )
    exp_gained_common = fields.Integer(
        string="Exp Guadagnata Comune",
        related="session_id.exp_gained_common",
        help="Esperienza che il player ha guadagnata in questa sessione. "
             "Comprende: Tesori/Info, Missione, Hex-Visti, Scontri/(Numero di player)."
    )
    exp_gained_total = fields.Integer(
        string="Exp Guadagnata Totale",
        compute="_compute_exp_gained_total",
        help="Esperienza che il player ha guadagnata in questa sessione. "
             "Comprende: Exp Guadagnata Comune + Exp Guadagnata Singola."
    )
    exp_gained_adj = fields.Integer(
        string="Exp Guadagnata Totale Adj",
        compute="_compute_exp_gained_adj",
        help="Differenza tra 'Exp Finale Adj' e 'Exp Iniziale'."
    )
    exp_end = fields.Integer(
        string="Exp Finale",
        compute="_compute_exp_end",
        help="Exp di questo PG a fine sessione."
    )
    exp_end_adj = fields.Integer(
        string="Exp Finale Adj",
        compute="_compute_exp_end_adj",
        help="Exp di questo PG a fine sessione, parificata alla soglia"
    )
    liv_end = fields.Integer(
        string="Livello Finale",
        compute="_compute_liv_end",
        help="Livello di questo PG a fine sessione."
    )
    # ------------------------------------------------------------------------------------------------------------------
    role = fields.Char(
        string="Ruolo",
        help="Ruolo che si assume nella spedizione (Cartografo, Leader, Scriba, etc...)"
    )
    role_percentage = fields.Float(
        string="Ruolo: impegno",
        help="Percentuale d'impegno nel ricoprire il ruolo (5%, 10% o 15%)"
    )
    role_exp = fields.Integer(
        string="Ruolo: Exp",
        compute="_compute_role_exp",
        help="Esperienza derivante dal Ruolo, proporzionale alla % d'impegno di quel player."
    )
    # ------------------------------------------------------------------------------------------------------------------
    help = fields.Char(
        string="Aiuto",
        help="Aiutare DM e altri player con ad esempio regole, gestione Task, mantenere ordine."
    )
    help_percentage = fields.Float(
        string="Aiuto: impegno",
        help="Percentuale d'impegno nell'aiutare il DM e gli altri player."
    )
    help_exp = fields.Integer(
        string="Aiuto: Exp",
        compute="_compute_help_exp",
        help="Esperienza derivante Aiutare DM e altri player, proporzionale alla % d'aiuto di quel player."
    )
    # ------------------------------------------------------------------------------------------------------------------
    rp = fields.Char(
        string="Role Play"
    )
    rp_percentage = fields.Float(
        string="Role Play: impegno",
        help="Percentuale d'impegno nel Role Play"
    )
    rp_exp = fields.Integer(
        string="Role Play: Exp",
        compute="_compute_rp_exp",
        help="Esperienza derivante dal Role Play, proporzionale alla % di Role Play di quel player."
    )
    date = fields.Date(
        string="Data",
        related="session_id.date",
    )
    state = fields.Selection(
        string="Stato",
        related="session_id.state",
    )

    # ------------------------------------------------------------------------------------------------------------------

    @api.onchange('pg_id')
    def _onchange_exp_start(self):
        self.exp_start = self.pg_id.exp if self.pg_id else 0

    @api.depends('exp_start')
    def _compute_liv_start(self):
        for rec in self:
            rec.liv_start = get_level_by_exp(rec.exp_start)

    @api.depends('liv_start')
    def _compute_exp_bar(self):
        for rec in self:
            rec.exp_bar = get_exp_bar(rec.liv_start)

    @api.depends('exp_start')
    def _compute_exp_next_level(self):
        for rec in self:
            rec.exp_next_level = get_exp_next_level(rec.exp_start)

    @api.depends('role_percentage', 'session_id.party_exp_bar')
    def _compute_role_exp(self):
        for rec in self:
            rec.role_exp = rec.session_id.party_exp_bar * rec.role_percentage if rec.session_id else 0

    @api.depends('help_percentage', 'session_id.party_exp_bar')
    def _compute_help_exp(self):
        for rec in self:
            rec.help_exp = rec.session_id.party_exp_bar * rec.help_percentage if rec.session_id else 0

    @api.depends('rp_percentage', 'session_id.party_exp_bar')
    def _compute_rp_exp(self):
        for rec in self:
            rec.rp_exp = rec.session_id.party_exp_bar * rec.rp_percentage if rec.session_id else 0

    @api.depends('role_exp', 'help_exp', 'rp_exp')
    def _compute_exp_gained_single(self):
        for rec in self:
            rec.exp_gained_single = rec.rp_exp + rec.help_exp + rec.role_exp

    @api.depends('exp_gained_common', 'exp_gained_single')
    def _compute_exp_gained_total(self):
        for rec in self:
            rec.exp_gained_total = rec.exp_gained_common + rec.exp_gained_single

    @api.depends('exp_start', 'exp_end_adj')
    def _compute_exp_gained_adj(self):
        for rec in self:
            rec.exp_gained_adj = rec.exp_end_adj - rec.exp_start

    @api.depends('exp_start', 'exp_gained_total')
    def _compute_exp_end(self):
        for rec in self:
            rec.exp_end = rec.exp_start + rec.exp_gained_single + rec.session_id.exp_gained_common

    @api.depends('session_id', 'exp_end')
    def _compute_exp_end_adj(self):
        for rec in self:
            exp_soglia = rec.session_id.exp_soglia if rec.session_id else 0
            rec.exp_end_adj = rec.exp_end if (exp_soglia < rec.exp_end) else exp_soglia

    @api.depends('exp_end_adj')
    def _compute_liv_end(self):
        for rec in self:
            rec.liv_end = get_level_by_exp(rec.exp_end_adj)
