from odoo import fields, models, api


class PointOfInterest(models.Model):
    _name = "point.of.interest"
    _description = "Point of Interest"

    # region FIELDS - BASE ---------------------------------------------------------------------------------------------
    name = fields.Char(
        string="Nome",
        required=True
    )
    description = fields.Html(
        string="Descrizione"
    )
    image = fields.Image(
        string="Immagine",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # region FIELD - NARRATIVE ENTITY ----------------------------------------------------------------------------------
    quest_ids = fields.Many2many(
        string="Missioni",
        comodel_name="quest.quest",
        relation="quest_poi_rel",
    )
    creature_ids = fields.Many2many(
        string="Creature",
        comodel_name="creature.creature",
        relation="poi_creature_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazione",
        comodel_name="creature.faction",
        relation="poi_faction_rel",
    )
    # endregion --------------------------------------------------------------------------------------------------------

    # category_id	Tipologia specifica (Many2one poi.category con valori “Naturale/Artificiale” e sottocategorie).
    # danger_level	Valore indicativo (es. SML/difficoltà).
    # status	Enum (concept, unlocked, cleared…) per gestire progressi.
    # todo lore_item_ids	Many2many → lore.item	Leggende, miti, oggetti collegati.
    # Record di categoria (Naturale, Artificiale, sottocategorie comuni).

    # Campi: name, hex_id (Many2one hex.hex), category_id, description, image, gallery_ids, danger_level, status, is_primary, notes
    # Relazioni: lore_item_ids

    # Popolamento iniziale di categorie (“Naturale”, “Artificiale” ecc.).
