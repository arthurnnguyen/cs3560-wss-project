# square.py
# Represents individual map tiles

class Square:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def has_food_bonus(self):
        from wss.item import FoodBonus
        return any(isinstance(item, FoodBonus) for item in self.items)

    def has_water_bonus(self):
        from wss.item import WaterBonus
        return any(isinstance(item, WaterBonus) for item in self.items)

    def has_gold_bonus(self):
        from wss.item import GoldBonus
        return any(isinstance(item, GoldBonus) for item in self.items)

    def has_trader(self):
        from wss.trader import Trader
        return any(isinstance(item, Trader) for item in self.items)

    def is_passable(self):
        # Optional — allow vision to evaluate square (for easiest_path)
        return self.terrain.move_cost <= 5  # tweak this if needed