import logging

from odoo import Command
from odoo import models


class CreatureEncounter(models.Model):
    _name = "creature.encounter"
    _inherit = ['creature.encounter', 'mixin.import.py']

    # def _popolate_by_py(self, modulo):
    #     """OVERRIDE: ..."""
    #     data_dicts = getattr(modulo, 'dicts', None)
    #     if data_dicts is None:
    #         raise ValueError(f"'dicts' not found")
    #
    #     LIST_ALREADY_EXIST = self.search([]).mapped('name')
    #     MAP_CREATURE_ID = self.get_map_model_id('creature.creature')
    #     MAP_FACTION_ID = self.get_map_model_id('creature.faction')
    #
    #     filtered_dicts = []
    #     for dikt in data_dicts:
    #         if dikt['name'] in LIST_ALREADY_EXIST:
    #             logging.warning(f"Il {self._name} {dikt['name']} esiste già")
    #             continue
    #         dikt['faction_id'] = MAP_FACTION_ID[dikt['faction_id']] if dikt['faction_id'] else False
    #         dikt['line_ids'] = [(0, 0, {
    #             'creature_qty': x['creature_qty'],
    #             'creature_id': MAP_CREATURE_ID[x['creature_id']] if x['creature_id'] else False
    #         }) for x in dikt['line_ids']]
    #         filtered_dicts.append(dikt)
    #     self.create(filtered_dicts)
    #
    # @staticmethod
    # def from_rec_to_dikt(rec):
    #     """OVERRIDE: Trasforma un record di Odoo in un dizionario che può essere salvato nell'apposito file data."""
    #     dikt = {
    #         'name': rec.name,
    #         'faction_id': rec.faction_id.name if rec.faction_id else False,
    #         "line_ids": [{
    #             'creature_qty': x.creature_qty,
    #             'creature_id': x.creature_id.name if x.creature_id else False
    #         } for x in rec.line_ids]
    #     }
    #
    #     return dikt


# region METODI DEPRECATI ------------------------------------------------------------------------------------------
def popolate_endemic_encounter(self):
    """Crea scontri per le creature con il tag endemico usando la tabella MAP_SML_QTY."""

    logging.info("DEPRECATE download_encounters_py")
    pass

    # Dizionario per creare degli scontri a SML X con solo creature di CR Y
    # Nella tupla sono riportate la quantity di creature di quel CR per ottenere quel SML
    # "SML": ("q_cr0125", "q_cr025", "q_cr05", "q_cr1", "q_cr2", "q_cr3", "q_cr4, "q_cr5", "q_cr6", "q_cr7", "q_cr8")
    LIST_CR = [0.125, 0.25, 0.5, 1, 2, 3, 4, 5, 6, 7, 8]
    MAP_SML_QTY = {
        "3": (16, 11, 7, 4, None, None, None, 1, None, None, None),
        "4": (20, 14, 9, 5, 3, 2, None, None, 1, None, None),
        "5": (45, 22, 14, 9, 5, 3, None, None, None, None, None),
        "6": (56, 28, 15, 10, 6, 4, None, 2, None, None, None),
        "7": (68, 33, 17, 11, None, 5, 3, None, 2, None, None),
        "8": (84, 42, 21, 14, 8, 6, 4, None, None, None, None),
        "9": (96, 48, 24, 15, 9, None, None, 3, None, None, None),
        "10": (120, 56, 28, 15, 10, 7, 5, None, None, None, 2),
    }

    logging.info("START popolate_endemic_encounter")
    for sml, qtys in MAP_SML_QTY.items():
        logging.info(f"** START SML {sml}")
        for i, qty in enumerate(qtys):
            if not qty or qty > 11:
                continue
            cr = LIST_CR[i]
            creatures = self.env["creature.creature"].search([("cr", "=", cr), ("is_endemic", "=", True)])
            logging.info(f"**** START SML {sml} - CR {cr} - FIND {len(creatures)} CREATURES")
            for n, creature in enumerate(creatures):
                encounter = self.search([("name", "=", f"Endemico: {qty} x {creature.name}")])
                if encounter:
                    logging.warning(f"*** ({n + 1}/{len(creatures)}) SKIP {encounter.name} - ALREADY EXISTS")
                    continue
                encounter = self.create({
                    "line_ids": [Command.create({
                        'creature_qty': qty,
                        'creature_id': creature.id
                    })]
                })
                logging.info(f"****** ({n + 1}/{len(creatures)}) CREATE {encounter.name}")
            logging.info(f"**** END SML {sml} - CR {cr}")
        logging.info(f"** END SML {sml}")
    logging.info("END popolate_endemic_encounter")
# endregion METODI DEPRECATI ---------------------------------------------------------------------------------------
