from odoo import fields, models, api
from ...cf_hex_biome.utility.exp import get_level_by_exp


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

    session_pg_ids = fields.One2many(
        comodel_name="campaign.session.pg",
        compute="_compute_session_pg_ids",
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
            last_session_pg = rec.session_pg_ids[0] if rec.session_pg_ids else None
            if not last_session_pg:
                rec.exp = 900
            else:
                rec.exp = last_session_pg.exp_end_adj if last_session_pg else rec.exp
