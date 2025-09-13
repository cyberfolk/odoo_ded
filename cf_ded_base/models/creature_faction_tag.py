from odoo import fields, models, api


class CreatureFactionTag(models.Model):
    _name = "creature.faction.tag"
    _description = "Tag per fazioni"

    name = fields.Char(
        string="Nome",
        required=True,
        help="Nome del Tag per fazioni"
    )

    faction_ids = fields.Many2many(
        comodel_name="creature.faction",
        relation="faction_tag_rel",
        string="Fazioni",
        help="Fazioni con questo tag"
    )
