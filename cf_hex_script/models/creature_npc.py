import logging

from odoo import fields, models, api, Command
from ...cf_hex_biome.utility.exp import MAP_CR_EXP

_logger = logging.getLogger(__name__)


class CreatureNpc(models.Model):
    _name = "creature.npc"
    _description = "NPC"

    name = fields.Char(
        string="Nome",
        required=True,
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
        comodel_name="faction.faction",
        relation="faction_faction_creature_npc_rel",
        string="Fazioni",
        help="Fazioni del NPC",
    )

    description = fields.Html(
        string="Descrizione",
        help="Descrizione della Creatura",
    )

    image_primary = fields.Image(
        string="Immagine",
    )

    creature_id = fields.Many2one(
        comodel_name="creature.creature",
        string="Creatura di riferimento",
    )

    #todo potrebbe essere m2m
    hex_script_id = fields.Many2one(
        comodel_name="hex.script",
        string="Hex Script",
    )

    @api.depends("cr")
    def _compute_exp(self):
        for record in self:
            record.exp = MAP_CR_EXP[str(record.cr)]
