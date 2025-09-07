from odoo import fields, models, api


class CreatureNpc(models.Model):
    _inherit = "creature.creature"

    # region FIELD - NARRATIVE ENTITY ----------------------------------------------------------------------------------
    npc_quest_ids = fields.Many2many(
        string="NPC Missioni",
        comodel_name="quest.quest",
        relation="quest_npc_rel",
        # column1="quest_id",
        # column2="npc_id",
    )
    npc_poi_ids = fields.Many2many(
        string="NPC Punto d'Interesse",
        comodel_name="point.of.interest",
        relation="poi_npc_rel",
        # column1="poi_id",
        # column2="npc_id",
    )
    npc_monster_ids = fields.Many2many(
        string="NPC Mostro Leggendario",
        comodel_name="creature.creature",
        relation="monster_npc_rel",
        column1="monster_id",
        column2="npc_id",
        domain=[("is_legendary", "=", True)],
    )
    npc_faction_ids = fields.Many2many(
        string="NPC Fazioni",
        comodel_name="creature.faction",
        relation="faction_npc_rel",
        # column1="faction_id",
        # column2="npc_id",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELD - DESCRIPTIVE ---------------------------------------------------------------------------------------
    titles = fields.Char(
        string="Titoli",
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
    # endregion --------------------------------------------------------------------------------------------------------
