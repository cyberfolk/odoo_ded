# Odoo | Hex Map

**Initial commit**: 21/01/24

**Stack**: Odoo, Owl, Python, JS, XML, HTML, CSS, SCSS e Bootstrap.

**Info**: :world_map: Repo che contiene App e Moduli per gestire una Hex Map.

- **cf_hex_base** In questa app vengono introdotti gli elementi base della Hex Map: ovvero Macro-area, Quadranti,
  Esagoni e AssetTiles.
- **cf_hex_biome** In questo modulo vengono introdotti i Biomi, Le Creature, Le Fazioni e gli Scontri.
- **cf_hex_lore** In questo modulo viene aggiunta la Lore sugli Hex mediante campi Descrizione, Immagini e altri campi
  relazionali che li collegano ai relativi biomi e alle creature che lo popolano.
- **cf_hex_client** In questo modulo viene introdotto:
    - Un'interfaccia per poter interagire direttamente con le mappe in modo più semplice.
    - Il widget "QuadWidget" per visualizzare la mappa dei quadranti nei relativi Form.
    - Il modello "asset_tile" che permette assegnare un immagine(Montagne/Alberi/Incroci/...) a uno specifico Hex.
- **cf_hex_data** In questo modulo vengono caricati i dati dei modelli introdotti negli altri moduli.

<img src="cf_hex_base/static/description/icon.png" width="250"/>
