import random

RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]

#(ab_runde, [common, uncommon, rare, epic, legendary])
ODDS_TABLE = [
    (1,  [60, 30, 10, 0, 0]),
    (4,  [35, 35, 25, 5, 0]),
    (8,  [20, 25, 35, 15, 5]),
    (13, [10, 20, 30, 25, 15]),
]

def weights_for_round(curRound):
    weights = ODDS_TABLE[0][1]
    for ab_runde, w in ODDS_TABLE:
        if curRound >= ab_runde:
            weights = w
    return weights

def roll_rarity(curRound):
    return random.choices(RARITIES, weights=weights_for_round(curRound))[0]
