from odoo import fields, models, api


class LoreItem(models.Model):
    """
    Documentazione completa:
        https://cyberfolk.github.io/wm-docs/md/lore-tool/l05-lore-item/
    """

    _name = "lore.item"
    _inherit = "mixin.narrative.entity"
    _description = "Lore Item"
    _rec_name = "complete_name"

    _sql_constraints = [
        ("unique_lore_item_name", "UNIQUE(name)", "Il nome del Lore Item deve essere univoco!"),
    ]

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    # ...
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - HIERARCHY -------------------------------------------------------------------------------------
    child_ids = fields.One2many(
        comodel_name="lore.item",
        inverse_name="parent_id",
        string="Lore Item figli",
    )
    parent_id = fields.Many2one(
        comodel_name="lore.item",
        string="Lore Item Padre",
    )
    complete_name = fields.Char(
        string="Nome Completo",
        compute="_compute_complete_name",
        store=True,
        recursive=True
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = f"{record.parent_id.complete_name} / {record.name}"
            else:
                record.complete_name = record.name

    @api.depends('complete_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.complete_name

    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELDS - NARRATIVE ENTITY ---------------------------------------------------------------------------------
    poi_ids = fields.Many2many(
        string="Punti d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_lore_item_rel",
    )
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="quest_lore_item_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazione",
        comodel_name="creature.faction",
        relation="lore_item_faction_rel",
    )
    settlement_ids = fields.Many2many(
        string="Insediamenti",
        comodel_name="settlement.settlement",
        relation="settlement_lore_item_rel",
    )
    artifact_ids = fields.Many2many(
        string="Artefatti",
        comodel_name="artifact.artifact",
        relation="artifact_lore_item_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="lore_item_creature_rel",
        domain=[('is_base', '=', True)]
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.creature",
        relation="lore_item_npc_rel",
        domain=[('is_npc', '=', True)]
    )
    monster_ids = fields.Many2many(
        string="Mostri Leggendari",
        comodel_name="creature.creature",
        relation="lore_item_monster_rel",
        domain=[('is_legendary', '=', True)]
    )
    # endregion --------------------------------------------------------------------------------------------------------
