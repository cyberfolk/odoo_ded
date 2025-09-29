from odoo import api, fields, models


class HexMixin(models.AbstractModel):
    _name = 'hex.mixin'
    _description = "Abstract class that contains common fields and common behaviors of the main hex-class"

    name = fields.Char(
        string='Name',
    )

    code = fields.Char(
        string='Code',
        compute='_compute_code',
    )

    index = fields.Integer(
        string='Index',
        help="Il valore di 'index' deve essere compreso tra 1 e 19.",
    )

    type = fields.Selection(
        selection=[],
        string="Tipo",
    )

    @api.depends('index', 'type')
    def _compute_code(self):
        for rec in self:
            code = rec.get_code()
            rec.code = code

    def get_code(self):
        self.ensure_one()
        code = 'void'
        return code

    @api.depends('code', 'name')
    def _compute_display_name(self):
        for rec in self:
            if rec.code and rec.name and rec.code != rec.name:
                rec.display_name = f"{rec.code} | {rec.name}"
            else:
                rec.display_name = rec.code or rec.name or "-"

    @api.constrains('name')
    def check_name(self):
        for record in self:
            if not record.name:
                record.name = record.code
