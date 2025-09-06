from odoo import fields, models, api
from ..utility.exp import MAP_CR_EXP


class CreatureNpc(models.Model):
    _name = "creature.npc"
    _description = "NPC"
    _inherit = "creature.stats"

    titles = fields.Char(
        string="Titoli",
    )

    cr = fields.Float(
        string="Grado Sfida",
        help="Grado sfida del NPC."
    )

    exp = fields.Float(
        string="Exp",
        compute="_compute_exp",
        help="Esperienza ottenuta eliminando la creatura."
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

    faction_ids = fields.Many2many(
        comodel_name="creature.faction",
        relation="creature_faction_creature_npc_rel",
        string="Fazioni",
        help="Fazioni del NPC",
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura di riferimento",
    )

    poi_ids = fields.Many2many(
        string="Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="point_of_interest_npc_rel",
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

    @api.depends("cr")
    def _compute_exp(self):
        for record in self:
            record.exp = MAP_CR_EXP[str(record.cr)]
