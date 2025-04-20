from odoo import fields, models, api
from ...cf_ded_base.utility.exp import get_level_by_exp


class CampaignPg(models.Model):
    _name = "campaign.pg"
    _description = "PG"

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

    player_id = fields.Many2one(
        comodel_name="res.partner",
        string="Player",
        domain="[('rpg_type', '=', 'player')]",
    )

    exp = fields.Integer(
        string="EXP",
        compute="_compute_exp",
        # default="900"
    )

    level = fields.Integer(
        string="Livello",
        compute="_compute_level",
    )

    race_s = fields.Selection(
        string="Razza",
        selection=[('HUMAN', 'Umano'), ('ELF', 'Elfo'), ('DWARF', 'Nano')],
    )

    class_s = fields.Selection(
        string="Classe",
        selection=[('WARRIOR', 'Guerriero'), ('MAGE', 'Mago'), ('RANGER', 'Cacciatore')],
    )

    campaign_id = fields.Many2one(
        comodel_name="campaign.campaign",
        string="Campagna",
    )

    session_pg_ids = fields.Many2many(
        comodel_name="campaign.session.pg",
        compute="_compute_session_pg_ids",
        store=True,
    )

    @api.depends('exp')
    def _compute_level(self):
        for rec in self:
            rec.level = get_level_by_exp(rec.exp)

    def _compute_session_pg_ids(self):
        for rec in self:
            rec.session_pg_ids = self.env['campaign.session.pg'].search([('pg_id', '=', rec.id)], order='id')

    @api.depends('session_pg_ids.exp_end_adj')
    def _compute_exp(self):
        for rec in self:
            session_pg_confirmed = rec.session_pg_ids.filtered(lambda x: x.state == 'confirmed')
            rec.exp = 900 + sum([x.exp_gained_adj for x in session_pg_confirmed])
