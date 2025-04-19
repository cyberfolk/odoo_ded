from odoo import fields, models


class SpellList(models.Model):
    _name = "spell.list"
    _description = "ListaIncantesimi"

    name = fields.Char(
        string="Name"
    )

    spell_ids = fields.Many2many(
        comodel_name='spell',
        string="Lista"
    )
