# ML | Mostro Leggendario

# Creatura unica o straordinariamente potente che caratterizza un esagono (o più) con la sua presenza,
# diventando una minaccia ecologica, un simbolo narrativo o una sfida epocale.

# - **NPC**: se la creatura è **interagibile socialmente** e ha **volontà autonoma**, allora può essere anche classificata come NPC (es. un drago antico parlante).
# - **Fazione**: se guida agenti o seguaci, diventa anche una fazione (tag utile: *leader-creatura*).
# - **Hex**: un **ML** può estendere la sua influenza oltre un singolo hex, ma il suo **cuore narrativo** resta localizzato.


from odoo import fields, models, api


class CreatureCreatureLegendary(models.Model):
    _inherit = "creature.creature"

    # region FIELD - NARRATIVE ENTITY ----------------------------------------------------------------------------------
    ml_quest_ids = fields.Many2many(
        string="ML Missioni",
        comodel_name="quest.quest",
        relation="quest_monster_rel",
        # column1="quest_id",
        # column2="monster_id",
    )
    ml_poi_ids = fields.Many2many(
        string="ML Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_monster_rel",
        # column1="poi_id",
        # column2="monster_id",
    )
    ml_npc_ids = fields.Many2many(
        string="ML NPCs",
        comodel_name="creature.creature",
        relation="monster_npc_rel",
        column1="monster_id",
        column2="npc_id",
        domain=[("is_npc", "=", True)],
    )
    ml_faction_ids = fields.Many2many(
        string="ML Fazioni",
        comodel_name="creature.faction",
        relation="monster_faction_rel",
        # column1="monster_id",
        # column2="faction_id",
    )
    # endregion --------------------------------------------------------------------------------------------------------
