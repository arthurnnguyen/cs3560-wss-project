# game.py
# Manages the setup and main game loop

from .map import Map
from .player import Player
from .trader import Trader
from .item import FoodBonus, WaterBonus, GoldBonus
from wss.vision import CautiousVision  # <-- Add this
# from wss.brain import SurvivalBrain  # Optional if you use AI later

DIRECTIONS = {
    'n': (0, 1),
    's': (0, -1),
    'e': (1, 0),
    'w': (-1, 0),
}

def prompt_command():
    while True:
        cmd = input("Enter command (n/s/e/w = move, r = rest, p = show path info, q = quit): ").strip().lower()
        if cmd in DIRECTIONS or cmd in ('r', 'q', 'p'):
            return cmd
        print("Invalid command. Try again.")

def main():
    print("=== Wilderness Survival System ===")

    # Validate width
    while True:
        try:
            width = int(input("Map width (number of squares): "))
            if width > 0:
                break
            print("Width must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Validate height
    while True:
        try:
            height = int(input("Map height (number of squares): "))
            if height > 0:
                break
            print("Height must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    # Validate difficulty
    valid_difficulties = {'easy', 'medium', 'hard'}
    while True:
        difficulty = input("Select difficulty (easy, medium, hard): ").strip().lower()
        if difficulty in valid_difficulties:
            break
        print("Invalid difficulty. Please enter 'easy', 'medium', or 'hard'.")

    game_map = Map(width, height, difficulty)
    print("\nGenerated map:")
    game_map.display()

    start_y = height // 2
    player = Player(
        max_strength=10,
        max_water=10,
        max_food=10,
        vision=CautiousVision(), 
        brain=None,
        location=(0, start_y)
    )

    # Example: place a Trader at (2, y)
    test_trader = Trader()
    game_map.get_square(2, start_y).add_item(test_trader)

    # Main game loop
    while True:
        x, y = player.location
        square = game_map.get_square(x, y)

        print(f"\nYou are at ({x}, {y}) on {square.terrain.name}.")
        print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}")

        # Interact with items/traders
        if square.items:
            for item in square.items[:]:
                print(f"There is a {type(item).__name__} here.")
                if isinstance(item, Trader):
                    player.trade_with(item)
                else:
                    player.collect(item)
                    print(f"Collected {type(item).__name__}.")
                    square.remove_item(item)

        # Check win/lose
        if player.location[0] >= width - 1:
            print("Congratulations! You've reached the east edge and survived!")
            break
        if player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
            print("You've run out of resources and perished. Game over.")
            break

        # Get command
        cmd = prompt_command()

        if cmd == 'q':
            print("Quitting game. Goodbye!")
            break
        elif cmd == 'r':
            player.rest()
            print("You rest for a turn (+2 strength, -0.5 food & water).")
        elif cmd == 'p':
            if player.vision:
                print("\n--- Path Info ---")

                path = player.vision.closest_food(game_map, player)
                if path:
                    print("[Path Info — Food]")
                    print(path)
                else:
                    print("[Path Info — Food] No valid path found.")

                path = player.vision.closest_water(game_map, player)
                if path:
                    print("[Path Info — Water]")
                    print(path)
                else:
                    print("[Path Info — Water] No valid path found.")

                path = player.vision.easiest_path(game_map, player)
                if path:
                    print("[Path Info — Easiest Path]")
                    print(path)
                else:
                    print("[Path Info — Easiest Path] No valid path found.")
            else:
                print("This player has no vision set.")
        else:
            dx, dy = DIRECTIONS[cmd]
            moved = player.move((dx, dy), game_map)
            if moved:
                print(f"You moved {cmd}.")
            else:
                print("Move failed; try a different direction or rest.")

if __name__ == '__main__':
    main()
