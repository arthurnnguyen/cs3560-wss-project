# terrain types and movement/food/water costs
import random


class Terrain:
    def __init__(self, name, move_cost, food_cost, water_cost):
        self.name = name
        self.move_cost = move_cost
        self.food_cost = food_cost
        self.water_cost = water_cost

    def short_code(self):
        return self.name[0].upper()


def generate_terrain_for_difficulty(difficulty):
    terrain_pool = {
        "easy": [
            Terrain("plains", 1, 1, 1),
            Terrain("forest", 2, 2, 2),
        ],
        "medium": [
            Terrain("plains", 1, 1, 1),
            Terrain("forest", 2, 2, 2),
            Terrain("swamp", 3, 3, 3),
            Terrain("mountain", 4, 3, 2),
        ],
        "hard": [
            Terrain("mountain", 4, 3, 2),
            Terrain("desert", 3, 2, 5),
            Terrain("swamp", 3, 3, 3),
            Terrain("forest", 2, 2, 2),
        ]
    }

    return random.choice(terrain_pool[difficulty])
