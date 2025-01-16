from odoo import fields, models

CAMPAIGN_STATE_LIST = [('active', 'Attiva'), ('closed', 'Chiusa')]


class CampaignCampaign(models.Model):
    _name = "campaign.campaign"
    _description = "Campagna"

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
        domain="[('rpg_type', '=', 'player')]",
    )

    pg_ids = fields.Many2many(
        comodel_name="campaign.pg",
        string="PG",
    )

    state = fields.Selection(
        string="Stato",
        selection=CAMPAIGN_STATE_LIST,
        default="active",
        help="Stato della campagna",
    )

    start_date = fields.Datetime(
        string="Data di inizio",
        help="Data di inizio della campagna",
    )

    end_date = fields.Datetime(
        string="Data di fine",
        help="Data di fine della campagna",
    )

    session_ids = fields.One2many(
        comodel_name="campaign.session",
        inverse_name="campaign_id",
        string="Sessioni",
    )
