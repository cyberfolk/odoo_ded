from odoo import fields, models

RPG_TYPE_SELECTION = [('master', 'Master'), ('player', 'Player')]


class CampaignSession(models.Model):
    _inherit = "res.partner"

    rpg_type = fields.Selection(
        string="Tipo",
        selection=RPG_TYPE_SELECTION,
        default='player'
    )

    pg_ids = fields.One2many(
        comodel_name="campaign.pg",
        inverse_name="player_id",
        string="PG",
    )
