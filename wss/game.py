# game.py
# Manages the setup and main game loop

from .map import Map
from .player import Player
from .trader import Trader
from .item import FoodBonus, WaterBonus, GoldBonus
from wss.vision import CautiousVision, FocusedVision, KeenEyed, FarSight
from wss.brain import SurvivalBrain, ResourceBrain, RiskyBrain

DIRECTIONS = {
    'n': (0, -1),
    's': (0, 1),
    'e': (1, 0),
    'w': (-1, 0),
}

def prompt_command():
    while True:
        cmd = input("Enter command (n=North, s=South, e=East, w=West, r=rest, p=path info, q=quit): ").strip().lower()
        if cmd in DIRECTIONS or cmd in ('r', 'q', 'p'):
            return cmd
        print("Invalid command. Please try again.")

def main():
    print("=== Wilderness Survival System ===")

    # Validate width
    while True:
        try:
            width = int(input("Map width (number of tiles): "))
            if width > 0:
                break
            print("Width must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            height = int(input("Map height (number of tiles): "))
            if height > 0:
                break
            print("Height must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    valid_difficulties = {'easy', 'medium', 'hard'}
    while True:
        difficulty = input("Choose difficulty (easy, medium, hard): ").strip().lower()
        if difficulty in valid_difficulties:
            break
        print("Invalid difficulty. Please enter 'easy', 'medium', or 'hard'.")

    game_map = Map(width, height, difficulty)
    print("\nMap generated:")
    game_map.display()

    start_y = height // 2

    print("\n=== Choose Vision Type ===")
    print("1. Focused Vision - Only sees the tile ahead")
    print("2. Cautious Vision - Sees forward, left, and right")
    print("3. Keen-Eyed - Sees multiple nearby tiles")
    print("4. Far-Sight - Sees farther")

    vision_choice = 0
    while vision_choice not in [1, 2, 3, 4]:
        try:
            vision_choice = int(input("Select vision type (1-4): "))
            if vision_choice not in [1, 2, 3, 4]:
                print("Invalid choice. Please choose between 1 and 4.")
        except ValueError:
            print("Please enter a number between 1 and 4.")

    vision = None
    if vision_choice == 1:
        vision = FocusedVision()
    elif vision_choice == 2:
        vision = CautiousVision()
    elif vision_choice == 3:
        vision = KeenEyed()
    elif vision_choice == 4:
        vision = FarSight()

    # Choose Brain (AI decision-making strategy)
    print("\n=== Choose Brain Type ===")
    print("1. Survival Brain - Prioritizes food and water")
    print("2. Resource Brain - Prioritizes gold and traders")
    print("3. Risky Brain - Prioritizes moving east at all costs")

    brain_choice = 0
    while brain_choice not in [1, 2, 3]:
        try:
            brain_choice = int(input("Select brain type (1-3): "))
            if brain_choice not in [1, 2, 3]:
                print("Invalid choice. Please choose between 1 and 3.")
        except ValueError:
            print("Please enter a number between 1 and 3.")

    # Create corresponding brain object
    brain = None
    if brain_choice == 1:
        brain = SurvivalBrain()
    elif brain_choice == 2:
        brain = ResourceBrain()
    elif brain_choice == 3:
        brain = RiskyBrain()
    # If 3 is chosen, brain remains None

    player = Player(
        max_strength=20,
        max_water=20,
        max_food=20,
        vision=vision,
        brain=brain,
        location=(0, start_y)
    )

    # Example: place a Trader at (2, y)
    test_trader = Trader()
    game_map.get_square(2, start_y).add_item(test_trader)

    # Show map with initial player position
    print("\nMap with player starting position:")
    game_map.display(player.location)

    # Track tiles already interacted with
    interacted_squares = set()

    # Main game loop
    while True:
        x, y = player.location
        square = game_map.get_square(x, y)
        current_pos = (x, y)

        print(f"\nYou are at position ({x}, {y}) on {square.terrain.name} terrain.")
        print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}")

        # Interact with items/traders if not already done on this square
        if current_pos not in interacted_squares:
            if square.items:
                for item in square.items[:]:
                    item_name = type(item).__name__
                    if item_name == "FoodBonus":
                        item_name = "Food"
                    elif item_name == "WaterBonus":
                        item_name = "Water"
                    elif item_name == "GoldBonus":
                        item_name = "Gold"
                    elif item_name == "Trader":
                        item_name = "Trader"

                    print(f"There is {item_name} here.")
                    if isinstance(item, Trader):
                        player.trade_with(item)
                    else:
                        player.collect(item)
                        print(f"Congrats! You collected {item_name}.")
                        square.remove_item(item)
            else:
                print("Unfortunately, there are no items on this tile.")

            # Mark this tile as interacted
            interacted_squares.add(current_pos)

        # Check win/lose conditions
        if player.location[0] >= width - 1:
            print("Congratulations! You've reached the east edge and survived!")
            break
        if player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
            print("You ran out of resources and did not survive. Game over.")
            break

        # Show map again
        print("\nCurrent map:")
        game_map.display(player.location)

        # Get player command
        cmd = prompt_command()

        if cmd == 'q':
            print("Exiting game. Goodbye!")
            break
        elif cmd == 'r':
            player.rest()
            print("You rested for one turn (+2 strength, -0.5 food & water).")
            print(f"Current stats -> Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}")
               elif cmd == 'p':
            if player.vision:
                print("\n--- Path Information ---")
                print(f"Vision type: {type(player.vision).__name__}")

                vision_type = type(player.vision).__name__

                # All vision types can find closest food
                path = player.vision.closest_food(game_map, player)
                if path:
                    print("[Info — Closest Food]")
                    print(f"From {path.start_position} to {path.end_position}")
                    print(f"Directions: {path.directions}")
                    print(f"Cost: {path.total_cost()}")
                else:
                    print("[Info — Food] No valid path found.")

                # All vision types can find closest water
                path = player.vision.closest_water(game_map, player)
                if path:
                    print("[Info — Closest Water]")
                    print(f"From {path.start_position} to {path.end_position}")
                    print(f"Directions: {path.directions}")
                    print(f"Cost: {path.total_cost()}")
                else:
                    print("[Info — Water] No valid path found.")

                # All vision types can find the easiest path
                path = player.vision.easiest_path(game_map, player)
                if path:
                    print("[Info — Easiest Path]")
                    print(f"From {path.start_position} to {path.end_position}")
                    print(f"Directions: {path.directions}")
                    print(f"Cost: {path.total_cost()}")
                else:
                    print("[Info — Easiest Path] No valid path found.")

                # Special vision types get more info
                if vision_type in ["KeenEyed", "FarSight"]:
                    # Closest gold (only for KeenEyed, FarSight)
                    path = player.vision.closest_gold(game_map, player)
                    if path:
                        print("[Info — Closest Gold]")
                        print(f"From {path.start_position} to {path.end_position}")
                        print(f"Directions: {path.directions}")
                        print(f"Cost: {path.total_cost()}")
                    else:
                        print("[Info — Gold] No valid path found.")

                if vision_type == "FarSight":
                    # Closest trader (only for FarSight)
                    path = player.vision.closest_trader(game_map, player)
                    if path:
                        print("[Info — Closest Trader]")
                        print(f"From {path.start_position} to {path.end_position}")
                        print(f"Directions: {path.directions}")
                        print(f"Cost: {path.total_cost()}")
                    else:
                        print("[Info — Trader] No valid path found.")

                    # Second closest food (only for FarSight)
                    path = player.vision.second_closest_food(game_map, player)
                    if path:
                        print("[Info — Alternate Food Option]")
                        print(f"From {path.start_position} to {path.end_position}")
                        print(f"Directions: {path.directions}")
                        print(f"Cost: {path.total_cost()}")

                # Check if any direction is possible
                can_move = False
                for direction in DIRECTIONS.values():
                    dx, dy = direction
                    new_x, new_y = x + dx, y + dy
                    if game_map.is_valid_position((new_x, new_y)):
                        new_square = game_map.get_square(new_x, new_y)
                        if new_square.is_passable():
                            can_move = True
                            break

                if not can_move:
                    print("\nWARNING: You cannot move in any direction from this position!")

                # If player has a brain, show suggestions
                if player.brain:
                    brain_type = type(player.brain).__name__
                    print(f"\n[Suggestion from {brain_type}]")
                    suggestion = player.brain.suggest_move(game_map, player)
                    if suggestion:
                        direction_names = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West', 'r': 'Rest'}
                        for direction, reason in suggestion.items():
                            if direction in direction_names:
                                if direction == 'r':
                                    print(f"- Suggest to {direction_names[direction]}: {reason}")
                                else:
                                    print(f"- Suggest moving {direction_names[direction]}: {reason}")
                    else:
                        print("- No suggestion. Consider resting or exploring.")
            else:
                print("This player has no vision.")
        else:
            dx, dy = DIRECTIONS[cmd]
            new_x, new_y = x + dx, y + dy

            # Check if the new position is valid
            if not game_map.is_valid_position((new_x, new_y)):
                print("Cannot move in that direction — out of map bounds!")
            else:
                new_square = game_map.get_square(new_x, new_y)
                if not new_square.is_passable():
                    print(f"Cannot move — terrain {new_square.terrain.name} is impassable!")
                else:
                    # Check if player has enough resources to move
                    terrain_cost = new_square.terrain.movement_cost()
                    if player.current_strength < terrain_cost['movement'] or \
                       player.current_food < terrain_cost['food'] or \
                       player.current_water < terrain_cost['water']:
                        print(f"Not enough resources to move! Required: Strength={terrain_cost['movement']}, "
                              f"Food={terrain_cost['food']}, Water={terrain_cost['water']}")
                    else:
                        moved = player.move((dx, dy), game_map)
                        if moved:
                            direction_names = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West'}
                            print(f"You moved {direction_names[cmd]}.")
                            print(f"Current stats -> Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}")
                            print("\nMap after moving:")
                            game_map.display(player.location)
                        else:
                            print("Failed to move; try another direction or rest.")

if __name__ == '__main__':
    main()