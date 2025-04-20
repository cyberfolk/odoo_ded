import logging

from odoo import fields, models, api
from ..utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureNpc(models.Model):
    _name = "creature.npc"
    _description = "NPC"

    name = fields.Char(
        string="Nome",
        required=True,
    )

    titles = fields.Char(
        string="Titoli",
    )

    _sql_constraints = [
        ('unique_creature_npc_name', 'UNIQUE(name)', 'Il nome del NPC deve essere univoco!')
    ]

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

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Creatura",
    )

    image = fields.Image(
        string="Immagine",
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura di riferimento",
    )

    @api.depends("cr")
    def _compute_exp(self):
        for record in self:
            record.exp = MAP_CR_EXP[str(record.cr)]
