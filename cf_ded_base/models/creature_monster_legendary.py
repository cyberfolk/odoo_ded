# ML | Mostro Leggendario

# Creatura unica o straordinariamente potente che caratterizza un esagono (o più) con la sua presenza,
# diventando una minaccia ecologica, un simbolo narrativo o una sfida epocale.

# - **NPC**: se la creatura è **interagibile socialmente** e ha **volontà autonoma**, allora può essere anche classificata come NPC (es. un drago antico parlante).
# - **Fazione**: se guida agenti o seguaci, diventa anche una fazione (tag utile: *leader-creatura*).
# - **Hex**: un **ML** può estendere la sua influenza oltre un singolo hex, ma il suo **cuore narrativo** resta localizzato.


from odoo import fields, models, api
from ..utility.exp import MAP_CR_EXP


class CreatureMonsterLegendary(models.Model):
    _name = "creature.monster.legendary"
    _inherit = "creature.base.mixin"
    _description = "Creature | Monster Legendary (ML)"

    # region M2M Entità narrative
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="quest_monster_rel",
    )
    poi_ids = fields.Many2many(
        string="Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_monster_rel",
    )
    npc_ids = fields.Many2many(
        string="NPCs",
        comodel_name="creature.npc",
        relation="monster_npc_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazioni",
        comodel_name="creature.faction",
        relation="monster_faction_rel",
    )
    # endregion
