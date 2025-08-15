from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class NarrativeRelation(models.Model):
    _name = "ded.narrative.relation"
    _description = "Narrative Relation"
    _inherit = ["mail.thread"]

    description = fields.Text(required=True, tracking=True)
    source_ref = fields.Reference(
        selection="_selection_reference_models", required=True, tracking=True
    )
    source_model = fields.Many2one("ir.model", required=True, index=True)
    source_id = fields.Integer(required=True, index=True)
    target_ref = fields.Reference(
        selection="_selection_reference_models", required=True, tracking=True
    )
    target_model = fields.Many2one("ir.model", required=True, index=True)
    target_id = fields.Integer(required=True, index=True)
    is_directional = fields.Boolean(default=True)
    name = fields.Char(compute="_compute_name", store=True)

    _sql_constraints = [
        (
            "no_self_link",
            "CHECK(source_model_id != target_model_id OR source_id != target_id)",
            "Source and target must be different.",
        )
    ]

    @api.depends("source_ref", "target_ref")
    def _compute_name(self):
        for record in self:
            source_name = record.source_ref.display_name if record.source_ref else ""
            target_name = record.target_ref.display_name if record.target_ref else ""
            record.name = f"{source_name} → {target_name}"

    @api.onchange("source_ref")
    def _onchange_source_ref(self):
        for record in self:
            if record.source_ref:
                record.source_model = self.env["ir.model"]._get(record.source_ref._name)
                record.source_id = record.source_ref.id
            else:
                record.source_model = False
                record.source_id = False

    @api.onchange("target_ref")
    def _onchange_target_ref(self):
        for record in self:
            if record.target_ref:
                record.target_model = self.env["ir.model"]._get(record.target_ref._name)
                record.target_id = record.target_ref.id
            else:
                record.target_model = False
                record.target_id = False

    @api.model
    def _get_allowed_model_names(self):
        param = (
            self.env["ir.config_parameter"].sudo().get_param(
                "ded.narrative.allowed_models", ""
            )
        )
        if param:
            return {m.strip() for m in param.split(",") if m.strip()}
        return set(
            self.env["ir.model"]
            .sudo()
            .search([("transient", "=", False)])
            .mapped("model")
        )

    @api.model
    def _selection_reference_models(self):
        allowed = sorted(self._get_allowed_model_names())
        models = self.env["ir.model"].sudo().search([("model", "in", allowed)])
        return [(m.model, m.name) for m in models]

    def _validate_allowed_models(self, model_names):
        allowed = self._get_allowed_model_names()
        if allowed:
            for model_name in model_names:
                if model_name not in allowed:
                    raise ValidationError(
                        _("Model %s is not allowed for narrative relations.")
                        % model_name
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("source_ref") and (
                not vals.get("source_model") or not vals.get("source_id")
            ):
                model_name, res_id = vals["source_ref"].split(",")
                vals["source_model"] = self.env["ir.model"]._get(model_name).id
                vals["source_id"] = int(res_id)
            if vals.get("target_ref") and (
                not vals.get("target_model") or not vals.get("target_id")
            ):
                model_name, res_id = vals["target_ref"].split(",")
                vals["target_model"] = self.env["ir.model"]._get(model_name).id
                vals["target_id"] = int(res_id)
            source_model_name = (
                self.env["ir.model"].browse(vals["source_model"]).model
                if vals.get("source_model")
                else False
            )
            target_model_name = (
                self.env["ir.model"].browse(vals["target_model"]).model
                if vals.get("target_model")
                else False
            )
            self._validate_allowed_models([source_model_name, target_model_name])
        return super().create(vals_list)

    def write(self, vals):
        if "source_ref" in vals:
            model_name, res_id = vals["source_ref"].split(",")
            vals["source_model"] = self.env["ir.model"]._get(model_name).id
            vals["source_id"] = int(res_id)
        if "target_ref" in vals:
            model_name, res_id = vals["target_ref"].split(",")
            vals["target_model"] = self.env["ir.model"]._get(model_name).id
            vals["target_id"] = int(res_id)
        for record in self:
            source_model_id = vals.get("source_model", record.source_model.id)
            target_model_id = vals.get("target_model", record.target_model.id)
            source_model_name = self.env["ir.model"].browse(source_model_id).model
            target_model_name = self.env["ir.model"].browse(target_model_id).model
            self._validate_allowed_models([source_model_name, target_model_name])
        return super().write(vals)
