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

    @api.depends('exp')
    def _compute_level(self):
        for rec in self:
            rec.level = get_level_by_exp(rec.exp)
