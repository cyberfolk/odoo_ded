import logging

from odoo import fields, api
from odoo import models
from ..utility.exp import MAP_QTY_MOD, MAP_LEVEL_EXP

_logger = logging.getLogger(__name__)


class CreatureEncounter(models.Model):
    _name = "creature.encounter"
    _description = "Scontro"

    # region FIELD -----------------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
        help="Nome dello scontro.",
        compute="_compute_name",
        store=True
    )

    line_ids = fields.One2many(
        comodel_name="creature.encounter.line",
        inverse_name="encounter_id",
        string="Linee",
        help="Linee dello scontro.",
    )

    exp_sum = fields.Integer(
        string="Exp Somma",
        compute="_compute_exp_sum",
        help="Somma delle esperienza delle singole creature.",
    )

    tot_creatures = fields.Integer(
        string="Totale Creature",
        compute="_compute_tot_creatures",
        help="Totale creature presenti nelle righe.",
    )

    exp_adj = fields.Integer(
        string="Exp Adjusted",
        compute="_compute_exp_adj",
        help="Esperienza dello scontro tenendo conto del modificatore per il numero di creature.",
    )

    sml = fields.Integer(
        string="SML",
        compute="_compute_sml",
        help="Scontro Mortale per 4 PG di Livello 'SML'",
        store=True,
    )

    creature_ids = fields.Many2many(
        comodel_name="creature.creature",
        compute="_compute_creature_ids",
        string="Creature",
        help="Creature che compongono lo scontro.",
    )

    biome_ids = fields.Many2many(
        comodel_name="biome.biome",
        relation="creature_encounter_biome_biome_rel",
        compute="_compute_biome_ids",
        string="Biomi",
        help="Biomi dove può verificarsi lo scontro.",
        store=True,
    )

    is_endemic = fields.Boolean(
        string="Endemico",
        compute="_compute_is_endemic",
        store=True,
    )

    faction_id = fields.Many2one(
        comodel_name="creature.faction",
        string="Fazione",
        help="Fazione dello scontro",
    )

    # endregion FIELD -------------------------------------------------------------------------------------------------

    # region COMPUTED METHOD -------------------------------------------------------------------------------------------
    @api.depends("line_ids", "faction_id")
    def _compute_is_endemic(self):
        for record in self:
            record.is_endemic = all(line.is_endemic for line in record.line_ids)
            if record.faction_id:
                record.is_endemic = False

    @api.depends("line_ids", "faction_id")
    def _compute_name(self):
        for record in self:
            record.name = " + ".join(filter(None, record.line_ids.mapped("name")))
            if record.faction_id:
                record.name = f"{record.faction_id.code}: {record.name}"
            elif record.is_endemic:
                record.name = f"Endemico: {record.name}"
            if not record.name:
                record.name = f"Nome temporaneo"

    @api.depends("line_ids")
    def _compute_exp_sum(self):
        for record in self:
            record.exp_sum = sum(line.exp_sum for line in record.line_ids)
            if not record.exp_sum:
                record.exp_sum = 0

    @api.depends("line_ids")
    def _compute_tot_creatures(self):
        for record in self:
            record.tot_creatures = sum(line.creature_qty for line in record.line_ids)
            if not record.tot_creatures:
                record.tot_creatures = 0

    @api.depends("line_ids")
    def _compute_exp_adj(self):
        for record in self:
            modificatore = MAP_QTY_MOD.get(str(record.tot_creatures), 4)
            record.exp_adj = record.exp_sum * modificatore
            if not record.exp_adj:
                record.exp_adj = 0

    @api.depends("line_ids")
    def _compute_sml(self):
        for record in self:
            MAP_SML_EXP = {k: v[3] * 4 for k, v in MAP_LEVEL_EXP.items()}
            steps = sorted(MAP_SML_EXP.values()) + [float('inf')]
            for i in range(len(steps) - 1):
                if steps[i] <= record.exp_adj < steps[i + 1]:
                    record.sml = i
                    break
            if not record.sml:
                self.sml = 0

    @api.depends("line_ids")
    def _compute_creature_ids(self):
        for record in self:
            for line in record.line_ids:
                record.creature_ids |= line.creature_id
            if not record.creature_ids:
                self.creature_ids = []

    @api.depends("line_ids")
    def _compute_biome_ids(self):
        for record in self:
            if record.creature_ids and record.creature_ids.biome_ids:
                record.biome_ids = record.creature_ids.biome_ids
            if not record.biome_ids:
                record.biome_ids = []  # or any other default value or action

    # endregion COMPUTED METHOD ----------------------------------------------------------------------------------------
