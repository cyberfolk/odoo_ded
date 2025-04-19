from odoo import fields, models


class Spell(models.Model):
    _name = "spell"
    _description = "Incantesimi"

    name = fields.Char(
        string="Nome",
    )
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Il nome deve essere univoco.')
    ]
    school = fields.Char(
        string="Scuola"
    )
    sub_school = fields.Char(
        string="Sotto-Scuola"
    )
    descriptors = fields.Char(
        string="Descrittori"
    )
    level = fields.Char(
        string="Livello"
    )
    components = fields.Char(
        string="Componenti"
    )
    casting_time = fields.Char(
        string="Tempo di lancio"
    )
    range = fields.Char(
        string="Raggio d'Azione"
    )
    target_area_effect = fields.Char(
        string="Bersaglio, area, effetto"
    )
    duration = fields.Char(
        string="Durata"
    )
    saving_throw = fields.Char(
        string="Tiro salvezza"
    )
    spell_resistance = fields.Char(
        string="Resistenza agli incantesimi"
    )
    description = fields.Html(
        string="Descrizione"
    )
    material_component = fields.Char(
        string="Componente materiale"
    )
    target = fields.Char(
        string="Target"
    )
    effect = fields.Char(
        string="Effetto"
    )
    area = fields.Char(
        string="Area"
    )
    base_spell = fields.Char(
        string="Base spell"
    )
    xp_cost = fields.Char(
        string="Costo XP"
    )
    focus = fields.Char(
        string="Focus"
    )
    blurb = fields.Char(
        string="Blurb"
    )
