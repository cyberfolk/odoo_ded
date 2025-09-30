from odoo import fields, models, api, Command


class HexMap(models.Model):
    _name = "hex.map"
    _description = "Mappa, contains Quadrants."

    name = fields.Char(
        string='Name',
    )

    quad_ids = fields.One2many(
        comodel_name='hex.quad',
        string="Quadrants",
        inverse_name='map_id',
    )

    type = fields.Selection(
        selection=[],
        string="Tipo",
    )

    # Campi usati sia da v2 che v3
    row_min = fields.Integer(string="Row Min", compute="compute_row_col")
    row_max = fields.Integer(string="Row Max", compute="compute_row_col")
    row_num = fields.Integer(string="Row Num", compute="compute_row_col")
    col_min = fields.Integer(string="Col Min", compute="compute_row_col")
    col_max = fields.Integer(string="Col Max", compute="compute_row_col")
    col_num = fields.Integer(string="Col Num", compute="compute_row_col")

    def compute_row_col(self):
        for rec in self:
            row_min, row_max, row_num, col_min, col_max, col_num = rec.get_row_col()
            rec.row_min = row_min
            rec.row_max = row_max
            rec.row_num = row_num
            rec.col_min = col_min
            rec.col_max = col_max
            rec.col_num = col_num

    def get_row_col(self):
        self.ensure_one()
        row_min = row_max = row_num = None
        col_min = col_max = col_num = None

        return row_min, row_max, row_num, col_min, col_max, col_num
