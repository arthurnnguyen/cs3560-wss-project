# map.py
# Creates and manages the map grid

from .square import Square
from .terrain import generate_terrain_for_difficulty
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

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

    def is_valid_position(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def display(self, player_location=None):
        
        for y, row in enumerate(self.grid):
            row_display = []
            for x, square in enumerate(row):
                terrain_code = square.terrain.short_code()
                if player_location and (x, y) == player_location:
                    row_display.append(f"{Back.YELLOW}{Fore.RED}{terrain_code}{Style.RESET_ALL}")
                else:
                    row_display.append(terrain_code)

            print(" ".join(row_display))
