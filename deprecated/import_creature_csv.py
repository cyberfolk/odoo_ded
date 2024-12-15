# METODO DEPRECATO PER IMPORTARE SCONTRI DA CSV

import csv
import logging
from pathlib import Path

from odoo import fields, Command

_logger = logging.getLogger(__name__)


# region METODI DEPRECATI ------------------------------------------------------------------------------------------
def popolate_faction_encounter(self):
    """Crea record partendo dal faction_encounter che deve essere presente nella cartella 'data'."""

    _logger.info("DEPRECATE popolate_faction_encounter")
    pass

    MAP_FACTION_ID = {x.name: x.id for x in self.env['creature.faction'].search([])}
    MAP_CREATURE_ID = {x.name: x.id for x in self.env['creature.creature'].search([])}
    name_file_csv = 'faction_encounter.csv'
    file_path = (Path(__file__).resolve().parents[1] / 'data' / name_file_csv).as_posix()
    with open(file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        i = 0
        for row in reader:
            i += 1
            faction_id = MAP_FACTION_ID.get(row['fazione'])
            list_creature_name = [row['c1'], row['c2'], row['c3'], row['c4']]
            list_creature_id = [MAP_CREATURE_ID[x] for x in list_creature_name if x]
            list_creature_number = [int(row['n1'] or 0), int(row['n2'] or 0), int(row['n3'] or 0),
                                    int(row['n4'] or 0)]

            lines = []
            for _id, num in zip(list_creature_id, list_creature_number):
                if (_id is None) != (num is None):
                    raise ValueError("Un elemento è `None` mentre l'altro è valorizzato.")
                if _id is not None and num is not None:
                    lines.append({
                        'creature_qty': num,
                        'creature_id': _id
                    })

            encounter = self.create({
                "faction_id": faction_id,
                "line_ids": [(fields.Command.create(line)) for line in lines]
            })
            print(f"{i} - {encounter.name} - {row['fazione']} - {list_creature_name} - {list_creature_number}")


def popolate_endemic_encounter(self):
    """Crea scontri per le creature con il tag endemico usando la tabella MAP_SML_QTY."""

    _logger.info("DEPRECATE download_encounters_py")
    pass

    _logger.info("START popolate_endemic_encounter")
    for sml, qtys in MAP_SML_QTY.items():
        _logger.info(f"** START SML {sml}")
        for i, qty in enumerate(qtys):
            if not qty or qty > 11:
                continue
            cr = LIST_CR[i]
            creatures = self.env["creature.creature"].search([("cr", "=", cr), ("is_endemic", "=", True)])
            _logger.info(f"**** START SML {sml} - CR {cr} - FIND {len(creatures)} CREATURES")
            for n, creature in enumerate(creatures):
                encounter = self.search([("name", "=", f"Endemico: {qty} x {creature.name}")])
                if encounter:
                    _logger.warning(f"*** ({n + 1}/{len(creatures)}) SKIP {encounter.name} - ALREADY EXISTS")
                    continue
                encounter = self.create({
                    "line_ids": [Command.create({
                        'creature_qty': qty,
                        'creature_id': creature.id
                    })]
                })
                _logger.info(f"****** ({n + 1}/{len(creatures)}) CREATE {encounter.name}")
            _logger.info(f"**** END SML {sml} - CR {cr}")
        _logger.info(f"** END SML {sml}")
    _logger.info("END popolate_endemic_encounter")
# endregion METODI DEPRECATI ---------------------------------------------------------------------------------------
