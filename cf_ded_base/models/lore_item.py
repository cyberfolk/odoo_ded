from odoo import fields, models, api


class LoreItem(models.Model):
    _name = "lore.item"
    _description = "Lore Item"

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
        required=True
    )
    description = fields.Html(
        string="Descrizione"
    )
    image = fields.Image(
        string="Immagine",
    )
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
        string="Insediamento",
        comodel_name="settlement.settlement",
        relation="settlement_lore_item_rel",
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
