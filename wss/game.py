# Manages the setup and main game loop

from .map import Map
from .player import Player
from .trader import Trader
from wss.brain import SurvivalBrain, RiskyBrain, ResourceBrain
from wss.vision import FocusedVision, KeenEyed, FarSight, CautiousVision

# You can add more Brain subclasses to this dict as you implement them
BRAIN_CHOICES = {
    'survival': SurvivalBrain,
    'risky': RiskyBrain,
    'resource': ResourceBrain,
}

# Vision style options
VISION_CHOICES = {
    'cautious': CautiousVision,
    'focused': FocusedVision,
    'keen': KeenEyed,
    'far': FarSight,
}

# Map Vision/Brain choice prompts to instances


def choose_option(prompt, options):
    keys = list(options.keys())
    while True:
        choice = input(f"{prompt} ({'/'.join(keys)}): ").strip().lower()
        if choice in options:
            return options[choice]()
        print(f"Invalid choice. Please select one of: {', '.join(keys)}.")


# Convert Path direction strings into (dx, dy) vectors
DIRECTION_MAP = {
    "MoveNorth": (0, -1),
    "MoveSouth": (0, 1),
    "MoveEast": (1, 0),
    "MoveWest": (-1, 0),
    "MoveNorthEast": (1, -1),
    "MoveNorthWest": (-1, -1),
    "MoveSouthEast": (1, 1),
    "MoveSouthWest": (-1, 1),
}


def main():
    print("=== Wilderness Survival System Simulation ===")

    # Map size and difficulty
    while True:
        try:
            width = int(input("Map width (squares): ").strip())
            height = int(input("Map height (squares): ").strip())
            if width > 0 and height > 0:
                break
            print("Width and height must be positive integers.")
        except ValueError:
            print("Please enter valid integers.")
    valid_diffs = ('easy', 'medium', 'hard')
    while True:
        diff = input("Select difficulty (easy, medium, hard): ").strip().lower()
        if diff in valid_diffs:
            difficulty = diff
            break
        print(f"Invalid choice. Choose: {', '.join(valid_diffs)}.")

    # AI configuration
    vision = choose_option("Select vision style", VISION_CHOICES)
    brain = choose_option("Select brain strategy", BRAIN_CHOICES)

    # Initialize map and player
    game_map = Map(width, height, difficulty)
    print("\nGenerated map:")
    game_map.display()

    start_y = height // 2
    player = Player(
        max_strength=10,
        max_water=10,
        max_food=10,
        vision=vision,
        brain=brain,
        location=(0, start_y)
    )

    turn = 1
    # Simulation loop
    while True:
        x, y = player.location
        square = game_map.get_square(x, y)

        # Collect bonuses or trade
        for item in square.items[:]:
            if isinstance(item, Trader):
                player.trade_with(item, turn)
            else:
                applied = item.apply_to(player, turn)
                if applied and not item.repeating:
                    square.remove_item(item)

        # Status
        print(f"\nTurn {turn}: Location {player.location} on {square.terrain.name}")
        print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, "
              f"Water: {player.current_water}, Gold: {player.current_gold}")

        # Win/Lose
        if player.location[0] >= width - 1:
            print("PLAYER WON: reached east edge!")
            break

        if player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
            print("PLAYER FAILED: resources depleted.")
            print("GAME OVER!")
            break

        # AI decision
        action = player.brain.make_move(player, game_map)
        print(f"Player action: {action}")

        # Execute
        if action == 'rest':
            player.rest()
        else:
            vec = DIRECTION_MAP.get(action)
            if vec:
                moved = player.move(vec, game_map)
                if not moved:
                    print("Move blocked; Player rests instead.")
                    player.rest()
            else:
                # Unrecognized command
                player.rest()

        turn += 1


if __name__ == '__main__':
    main()
