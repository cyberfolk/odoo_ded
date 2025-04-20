MAP_CR_EXP = {
    "0.0": 0,
    "0": 0,
    "0.125": 25,
    "0.25": 50,
    "0.5": 100,
    "1.0": 200,
    "2.0": 450,
    "3.0": 700,
    "4.0": 1100,
    "5.0": 1800,
    "6.0": 2300,
    "7.0": 2900,
    "8.0": 3900,
    "9.0": 5000,
    "10.0": 5900,
    "11.0": 7500,
    "12.0": 8400,
    "13.0": 10000,
    "14.0": 11500,
    "15.0": 13000,
    "16.0": 15000,
    "17.0": 18000,
    "18.0": 20000,
    "19.0": 22000,
    "20.0": 25000,
    "21.0": 33000,
    "22.0": 41000,
    "23.0": 50000,
    "24.0": 62000,
    "25.0": 75000,
    "26.0": 90000,
    "27.0": 105000,
    "28.0": 120000,
    "29.0": 135000,
    "30.0": 155000,
}

MAP_QTY_MOD = {
    "0": 0,
    "1": 1,
    "2": 1.5,
    "3": 2,
    "4": 2,
    "5": 2,
    "6": 2,
    "7": 2.5,
    "8": 2.5,
    "9": 2.5,
    "10": 2.5,
    "11": 3,
    "12": 3,
    "13": 3,
    "14": 3,
    "15": 4,
    "16": 4,
    "17": 4,
    "18": 4,
    "19": 4,
    "20": 4,
}

# Dizionario che collega "1 PG di liv " all'exp che avrebbe con 1 Scontro
# "Easy", "Medium", "Hard", "Deadly" e il "Daily Budget" ovvero l'exp massima che potrebbe accumulare in una giornata
# "livello_PG": ("Easy", "Medium", "Hard", "Deadly", "Daily Budget")
MAP_LEVEL_EXP = {
    "0": (0, 0, 0, 0, 0),
    "1": (25, 50, 75, 100, 300),
    "2": (50, 100, 150, 200, 600),
    "3": (75, 150, 225, 400, 1200),
    "4": (125, 250, 375, 500, 1700),
    "5": (250, 500, 750, 1100, 3500),
    "6": (300, 600, 900, 1400, 4000),
    "7": (350, 750, 1100, 1700, 5000),
    "8": (450, 900, 1400, 2100, 6000),
    "9": (550, 1100, 1600, 2400, 7500),
    "10": (600, 1200, 1900, 2800, 9000),
    "11": (800, 1600, 2400, 3600, 10500),
    "12": (1000, 2000, 3000, 4500, 11500),
    "13": (1100, 2200, 3400, 5100, 13500),
    "14": (1250, 2500, 3800, 5700, 15000),
    "15": (1400, 2800, 4300, 6400, 18000),
    "16": (1600, 3200, 4800, 7200, 20000),
    "17": (2000, 3900, 5900, 8800, 25000),
    "18": (2100, 4200, 6300, 9500, 27000),
    "19": (2400, 4900, 7300, 10900, 30000),
    "20": (2800, 5700, 8500, 12700, 40000),
}

MAP_LEVEL_EXP_PG = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
    11: 85000,
    12: 100000,
    13: 120000,
    14: 140000,
    15: 165000,
    16: 195000,
    17: 225000,
    18: 265000,
    19: 305000,
    20: 355000,
}


def get_level_by_exp(exp):
    """
    Calcola il livello di un personaggio (PG) basato sull'esperienza (EXP) secondo D&D 5e.

    :param exp: int - Punti esperienza del personaggio
    :return: int - Livello del personaggio
    """
    livello = 1
    for lvl, soglia in sorted(MAP_LEVEL_EXP_PG.items()):
        if exp >= soglia:
            livello = lvl
        else:
            break

    return livello


def get_exp_bar(livello):
    """
    Calcola la barra di esperienza necessaria per salire al livello successivo in D&D 5e.

    :param livello: int - Il livello attuale del personaggio (1-19)
    :return: tuple - Esperienza attuale minima e totale necessaria per il prossimo livello (exp_min, exp_totale)
    """
    if livello < 1 or livello >= 20:
        raise ValueError("Il livello deve essere compreso tra 1 e 19 (inclusi).")

    # Esperienza attuale minima per il livello corrente
    exp_min = MAP_LEVEL_EXP_PG[livello]
    # Esperienza totale necessaria per raggiungere il livello successivo
    exp_totale = MAP_LEVEL_EXP_PG[livello + 1]

    exp_bar = exp_totale - exp_min
    return exp_bar


def get_exp_next_level(exp):
    """
    Calcola l'esperienza minima necessaria per il livello successivo rispetto all'attuale esperienza.

    :param exp: int - Punti esperienza attuali del personaggio
    :return: int - Esperienza minima necessaria per il livello successivo
    """
    # Trova il livello corrente
    livello_attuale = 1
    for lvl, soglia in sorted(MAP_LEVEL_EXP_PG.items()):
        if exp >= soglia:
            livello_attuale = lvl
        else:
            break

    # Controlla se il livello successivo è disponibile
    if livello_attuale >= 20:
        return None  # Nessun livello successivo, il personaggio è al massimo livello

    # Esperienza minima necessaria per il livello successivo
    exp_prossimo = MAP_LEVEL_EXP_PG[livello_attuale + 1]

    return exp_prossimo


def get_budget_exp(level_list):
    """Calcola l'esperienza Scontro Easy, Scontro Medium, Scontro Hard, Scontro Deadly e Daily Budget del party inteso
    come somma dei parametri calcolati sui singoli livelli dei membri del party

    :param level_list: list - Lista dei livelli dei PG
    :return: tuple - (Easy, Medium, Hard, Deadly, Budget) livelli di esperienza relativi al party.
    """
    Easy, Medium, Hard, Deadly, Budget = 0, 0, 0, 0, 0
    for pg in level_list:
        easy, medium, hard, deadly, budget = MAP_LEVEL_EXP[f'{pg}']
        Easy += easy
        Medium += medium
        Hard += hard
        Deadly += deadly
        Budget += budget
    return Easy, Medium, Hard, Deadly, Budget
