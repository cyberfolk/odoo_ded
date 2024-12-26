import logging

from odoo import models

_logger = logging.getLogger(__name__)


class FactionFaction(models.Model):
    _name = "creature.faction"
    _inherit = ['creature.faction', 'mixin.import.py']

    def get_data_json(self):
        """Recupera i dati del modello in formato stringa."""
        _logger.info("START get_data_json")

        # Fetch faction and structure the data
        factions = self.search([])
        faction_list = [{
            'name': faction.name,
            'code': faction.code,
            'state': faction.state,
            'cosmology': faction.cosmology,
            'description': str(faction.description),
            'good_evil_axis': faction.good_evil_axis,
            "n01_years_in_region": faction.n01_years_in_region,
            "n02_daily_operations": faction.n02_daily_operations,
            "n03_feeding_habits": faction.n03_feeding_habits,
            "n04_handling_threats": faction.n04_handling_threats,
            "n05_answering_powers": faction.n05_answering_powers,
            "n06_scouts": faction.n06_scouts,
            "n07_key_positions_controlled": faction.n07_key_positions_controlled,
            "n08_boundary_marking": faction.n08_boundary_marking,
            "n09_territory_claiming": faction.n09_territory_claiming,
            "n10_base_structure": faction.n10_base_structure,
            "n11_base_origin": faction.n11_base_origin,
            "n12_base_purpose": faction.n12_base_purpose,
            "n13_long_term_goals": faction.n13_long_term_goals,
            "n14_short_term_goals": faction.n14_short_term_goals,
            "n15_motivations": faction.n15_motivations,
            "n16_goal_strategy": faction.n16_goal_strategy,
            "n17_leader_view_of_pcs": faction.n17_leader_view_of_pcs,
            "n18_contact_with_pcs": faction.n18_contact_with_pcs,
            "n19_possible_developments": faction.n19_possible_developments,
            "n20_faction_theme": faction.n20_faction_theme,
            "creature_names": [x.name for x in faction.creature_ids] if faction.creature_ids else None
        } for faction in factions]

        faction_childs_parents = [{
            'name': faction.name,
            'parent_name': faction.parent_id.name if faction.parent_id else None,
            'child_names': [x.name for x in faction.child_ids] if faction.child_ids else None,
        } for faction in factions]

        dat_str = (f'faction_dikts = {faction_list}\n'
                   f'parent_dikts = {faction_childs_parents}')
        return dat_str

    def _popolate_by_py(self, modulo):
        # Restituisci il dizionario dal modulo
        faction_dikts = getattr(modulo, 'faction_dikts', None)
        parent_dikts = getattr(modulo, 'parent_dikts', None)
        if faction_dikts is None:
            raise ValueError(f"'factions' not found in {name_file}")
        if parent_dikts is None:
            raise ValueError(f"'faction_childs_parents' not found in {name_file}")

        MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}
        LIST_FACTIONS_ALREADY_EXIST = self.env['creature.faction'].search([]).mapped('name')

        # Creo le fazioni e le salvo in factions
        filtered_factions_dikt = []
        for faction in faction_dikts:
            if faction['name'] in LIST_FACTIONS_ALREADY_EXIST:
                logging.warning(f"La fazione {faction['name']} esiste già (pt1)")
                continue
            if faction['creature_names']:
                faction['creature_ids'] = [MAP_CREATURE_ID.get(x) for x in faction['creature_names']]
            faction.pop('creature_names', None)
            filtered_factions_dikt.append(faction)
        factions = self.create(filtered_factions_dikt)

        # Ciclo le fazioni per associare gli opportuni parent_id e child_ids
        for parent_info in parent_dikts:
            if parent_info['name'] in LIST_FACTIONS_ALREADY_EXIST:
                logging.warning(f"La fazione {parent_info['name']} esiste già (pt2)")
                continue
            if parent_info.get('child_names'):
                child_records = self.env['creature.faction'].search([('name', 'in', parent_info['child_names'])])
                parent_info['child_ids'] = [(6, 0, child_records.ids)] if child_records else []

            if parent_info.get('parent_name'):
                parent_record = self.env['creature.faction'].search([('name', '=', parent_info['parent_name'])])
                parent_info['parent_id'] = parent_record.id if parent_record else None

            faction_record = factions.filtered(lambda x: x.name == parent_info['name'])
            if faction_record:
                faction_record.write({
                    'parent_id': parent_info.get('parent_id', []),
                    'child_ids': parent_info.get('child_ids', []),
                })


# MODEL STRUCTURE ------------------------------------------------------------------------------------------------------
# dikt_fields = {
#     'name':                           ('char', None),
#     'code':                           ('char', None),
#     'description':                    ('html', None),
#     'n01_years_in_region':            ('text', None),
#     'n02_daily_operations':           ('text', None),
#     'n03_feeding_habits':             ('text', None),
#     'n04_handling_threats':           ('text', None),
#     'n05_answering_powers':           ('text', None),
#     'n06_scouts':                     ('text', None),
#     'n07_key_positions_controlled':   ('text', None),
#     'n08_boundary_marking':           ('text', None),
#     'n09_territory_claiming':         ('text', None),
#     'n10_base_structure':             ('text', None),
#     'n11_base_origin':                ('text', None),
#     'n12_base_purpose':               ('text', None),
#     'n13_long_term_goals':            ('text', None),
#     'n14_short_term_goals':           ('text', None),
#     'n15_motivations':                ('text', None),
#     'n16_goal_strategy':              ('text', None),
#     'n17_leader_view_of_pcs':         ('text', None),
#     'n18_contact_with_pcs':           ('text', None),
#     'n19_possible_developments':      ('text', None),
#     'n20_faction_theme':              ('text', None),
#     'state':                          ('selection', None),
#     'good_evil_axis':                 ('selection', None),
#     'cosmology':                      ('selection', None),
#     'child_ids':                      ('one2many',  'creature.faction'),
#     'parent_id':                      ('many2one',  'creature.faction'),
#     'encounter_ids':                  ('one2many',  'creature.encounter'),
#     'creature_ids':                   ('many2many', 'creature.creature'),
#     'npc_ids':                        ('many2many', 'creature.npc'),
#     'hex_ids':                        ('many2many', 'hex.hex')
# }
