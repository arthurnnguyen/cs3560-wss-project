# Manages the setup and main game loop

from .map import Map
from .player import Player
from .trader import Trader
from .item import FoodBonus, WaterBonus, GoldBonus

# Direction vectors: n, s, e, w
DIRECTIONS = {
    'n': (0, -1),
    's': (0, 1),
    'e': (1, 0),
    'w': (-1, 0),
}


def prompt_command():
    while True:
        cmd = input("\nEnter command (n/s/e/w = move, r = rest, q = quit): ").strip().lower()
        if cmd in DIRECTIONS or cmd in ('r', 'q'):
            return cmd
        print("Invalid command. Try again.")


def main():
    print("=== Wilderness Survival System ===")

    # Validate width
    while True:
        raw = input("Map width (number of squares): ").strip()
        try:
            width = int(raw)
            if width > 0:
                break
            else:
                print("Width must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

    # Validate height
    while True:
        raw = input("Map height (number of squares): ").strip()
        try:
            height = int(raw)
            if height > 0:
                break
            else:
                print("Height must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

    # Validate difficulty
    valid_diffs = ("easy", "medium", "hard")
    while True:
        difficulty = input("Select difficulty (easy, medium, hard): ").strip().lower()
        if difficulty in valid_diffs:
            break
        print(f"Invalid choice. Please enter one of: {', '.join(valid_diffs)}.")
    print(f"Got it — map {width}×{height} on '{difficulty}' difficulty.")

    game_map = Map(width, height, difficulty)
    print("\nGenerated map:")
    game_map.display()

    # Initialize player at west edge, middle row
    start_y = height // 2
    player = Player(
        max_strength=10,
        max_water=10,
        max_food=10,
        vision=None,
        brain=None,
        location=(0, start_y)
    )

    # Main game loop
    while True:
        x, y = player.location
        square = game_map.get_square(x, y)

        for item in square.items[:]:
            if isinstance(item, Trader):
                player.trade_with(item)  # trader logic never gets removed
            else:
                applied = item.apply_to(player)
                if applied and not item.repeating:
                    square.remove_item(item)

        # Display status
        print(f"\nYou are at ({x}, {y}) on {square.terrain.name}.")
        print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, "
              f"Water: {player.current_water}, Gold: {player.current_gold}")

        # Collect or trade items in current square
        if square.items:
            for item in square.items[:]:
                print(f"\nThere is a {type(item).__name__} here.")
                if isinstance(item, Trader):
                    player.trade_with(item)
                else:
                    player.collect(item)
                    print(f"Collected {type(item).__name__}.")
                    square.remove_item(item)

        # Check for win / lose conditions
        if player.location[0] >= width - 1:
            print("Congratulations! You've reached the east edge and survived!")
            break
        if player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
            print("You've run out of resources and perished.\n")
            print("GAME OVER.")
            break

        # Get player command
        cmd = prompt_command()
        if cmd == 'q':
            print("Quitting game. Goodbye!")
            break
        elif cmd == 'r':
            player.rest()
            print("You rest for a turn (+2 strength, -0.5 food & water).")
        else:
            if cmd in DIRECTIONS:
                dx, dy = DIRECTIONS[cmd]
                moved = player.move((dx, dy), game_map)
                if moved:
                    print(f"You moved {cmd}.")


if __name__ == '__main__':
    main()
