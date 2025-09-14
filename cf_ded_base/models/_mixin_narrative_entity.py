from odoo import fields, models, api
from ..utility.narrative_entity import PREFIX_BY_MODE_MAP
from odoo.addons.http_routing.models.ir_http import slugify_one


class NarrativeEntityMixin(models.AbstractModel):
    _name = "mixin.narrative.entity"
    _description = "Mixin | Entità Narrative"

    name = fields.Char(
        string="Nome",
    )

    description = fields.Html(
        string="Descrizione",
    )

    image = fields.Image(
        string="Immagine",
    )

    code = fields.Char(
        string="Codice",
        compute='_compute_code',
        store=True,
    )

    @api.depends("name")
    def _compute_code(self):
        PREFIX = PREFIX_BY_MODE_MAP[self._name]
        for record in self:
            record.code = f"{PREFIX}_{slugify_one(record.name)}"
