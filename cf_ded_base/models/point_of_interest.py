from odoo import fields, models, api


class PointOfInterest(models.Model):
    _name = "point.of.interest"
    _description = "Point of Interest"

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
    quest_ids = fields.Many2many(
        string="Quest",
        comodel_name="quest.quest",
        relation="point_of_interest_quest_rel",
    )
    npc_ids = fields.Many2many(
        string="NPC",
        comodel_name="creature.npc",
        relation="point_of_interest_npc_rel",
    )
    faction_ids = fields.Many2many(
        string="Fazione",
        comodel_name="creature.faction",
        relation="point_of_interest_faction_rel",
    )

    # todo mostro leggendario
    # monster_id = fields.Many2one(
    #     string="Creatura",
    #     comodel_name="creature.creature",
    # )

# category_id	Tipologia specifica (Many2one poi.category con valori “Naturale/Artificiale” e sottocategorie).
# danger_level	Valore indicativo (es. SML/difficoltà).
# status	Enum (concept, unlocked, cleared…) per gestire progressi.
# todo hex_id	Many2one → hex.hex	Localizzazione (1 hex → 1 POI principale).
# todo lore_item_ids	Many2many → lore.item	Leggende, miti, oggetti collegati.
# Campo “scoperto” per distinguere POI noti o segreti ai PG.
# Record di categoria (Naturale, Artificiale, sottocategorie comuni).

# Campi: name, hex_id (Many2one hex.hex), category_id, description, image, gallery_ids, danger_level, status, is_primary, notes
# Relazioni: lore_item_ids

# Popolamento iniziale di categorie (“Naturale”, “Artificiale” ecc.).




