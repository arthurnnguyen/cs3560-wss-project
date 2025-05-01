# Creates and manages the map grid

from .square import Square
from .terrain import generate_terrain_for_difficulty

class Map:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

        self.generate_map(difficulty)

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
