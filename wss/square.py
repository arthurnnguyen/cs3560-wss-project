# Represents individual map tiles
from wss.item import FoodBonus, WaterBonus, GoldBonus
from wss.trader import Trader


class Square:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items = []  # food, water, gold, or Trader

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def is_passable(self):
        """Return True if the square can be entered. Always True unless you add impassable terrain."""
        return True

    def has_food_bonus(self):
        return any(isinstance(i, FoodBonus) for i in self.items)

    def has_water_bonus(self):
        return any(isinstance(i, WaterBonus) for i in self.items)

    def has_gold_bonus(self):
        return any(isinstance(i, GoldBonus) for i in self.items)

    def has_trader(self):
        return any(isinstance(i, Trader) for i in self.items)
