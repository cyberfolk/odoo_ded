from odoo import api, fields, models, _


class NarrativeRelationMixin(models.AbstractModel):
    _name = 'narrative.relation.mixin'
    _description = 'Mixin to display and manage narrative relations from a record'

    narrative_relations_count = fields.Integer(compute='_compute_narrative_relations_count')

    # Dominio “io sono source o io sono target”
    def _get_narrative_domain(self):
        self.ensure_one()
        return ['|', '&',
                ('source_model_name', '=', self._name), ('source_id', '=', self.id),
                '&', ('target_model_name', '=', self._name), ('target_id', '=', self.id)]

    def _compute_narrative_relations_count(self):
        Rel = self.env['narrative.relation'].sudo()
        for rec in self:
            rec.narrative_relations_count = Rel.search_count(rec._get_narrative_domain())

    def _action_open_narratives(self, direction=None):
        """Apri l’elenco delle relazioni che mi riguardano.
        direction: None (solo lista), 'out' (crea precompilando source), 'in' (crea precompilando target)"""
        self.ensure_one()
        ctx = dict(self.env.context or {})
        ctx.update({
            'relation_direction': direction,  # usato da default_get
            'active_model': self._name,
            'active_id': self.id,
        })
        view = {
            'type': 'ir.actions.act_window',
            'name': _('Relazioni'),
            'res_model': 'narrative.relation',
            'view_mode': 'form' if direction else 'tree,form',
            'domain': self._get_narrative_domain(),
            'context': ctx,
            'target': 'current',
        }
        return view

    # Bottoni da richiamare in XML
    def action_open_narratives(self):
        return self._action_open_narratives(direction=None)

    def action_add_outgoing_narrative(self):
        return self._action_open_narratives(direction='out')

    def action_add_incoming_narrative(self):
        return self._action_open_narratives(direction='in')
