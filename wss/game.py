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
    """
    Prompt the user for a command: move, rest, or quit.
    Returns:
        cmd (str): one of 'n','s','e','w','r','q'
    """
    while True:
        cmd = input("Enter command (n/s/e/w = move, r = rest, q = quit): ").strip().lower()
        if cmd in DIRECTIONS or cmd in ('r', 'q'):
            return cmd
        print("Invalid command. Try again.")


def main():
    print("=== Wilderness Survival System ===")
    # Initialize map
    width = int(input("Map width (number of squares): "))
    height = int(input("Map height (number of squares): "))
    difficulty = input("Select difficulty (easy, medium, hard): ").strip().lower()

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

    # Example: place a Trader at x=2, y=start_y for testing
    test_trader = Trader()
    game_map.get_square(2, start_y).add_item(test_trader)


    # Main game loop
    while True:
        x, y = player.location
        square = game_map.get_square(x, y)

        # Display status
        print(f"\nYou are at ({x}, {y}) on {square.terrain.name}.")
        print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}")

        # Collect or trade items in current square
        if square.items:
            for item in square.items[:]:
                print(f"There is a {type(item).__name__} here.")
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
            print("You've run out of resources and perished. Game over.")
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
                else:
                    print("You can't move there!")


if __name__ == '__main__':
    main()
