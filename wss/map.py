# Creates and manages the map grid
import random

from .item import WaterBonus, FoodBonus, GoldBonus
from .square import Square
from .terrain import generate_terrain_for_difficulty
from .trader import Trader


class Map:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

        self.generate_map(difficulty)
        self.place_items()    # ← populate bonuses & traders here


    def generate_map(self, difficulty):
        for y in range(self.height):
            for x in range(self.width):
                terrain = generate_terrain_for_difficulty(difficulty)
                self.grid[y][x] = Square(x, y, terrain)

    def get_square(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def display(self):
        for row in self.grid:
            print(" ".join(square.terrain.short_code() for square in row))

    def is_valid_position(self, coords):
        """
        Return True if coords is inside the map bounds.
        """
        x, y = coords
        return self.get_square(x, y) is not None

    def place_items(self):
        for y in range(self.height):
            for x in range(self.width):
                square = self.grid[y][x]

                # Skip the starting column (west edge) so players don't get freebies immediately
                if x == 0:
                    continue

                # One‐time food cache (10% chance)
                if random.random() < 0.50:
                    square.add_item(FoodBonus(amount=5, repeating=False))

                # Repeating water source (like a stream) (20% chance)
                if random.random() < 0.50:
                    square.add_item(WaterBonus(amount=3, repeating=True))

                # One‐time gold nugget (5% chance)
                if random.random() < 0.15:
                    square.add_item(GoldBonus(amount=2, repeating=False))

                # Trader (3% chance)
                if random.random() < 0.40:
                    square.add_item(Trader())
