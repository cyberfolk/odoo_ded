from odoo import models


class QuestQuest(models.Model):
    _inherit = ['quest.quest', 'narrative.relation.mixin']
    _name = 'quest.quest'
