import random


def select_grimoire():
    grimoires = [
        "Una Hoja",
        "Dos Hojas",
        "Tres Hojas",
        "Cuatro Hojas",
        "Cinco Hojas",
    ]
    weights = [0.3, 0.3, 0.2, 0.15, 0.05]
    return random.choices(grimoires, weights=weights, k=1)[0]
