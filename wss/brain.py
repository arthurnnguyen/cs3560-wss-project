# brain.py
# Player decision making strategy
import heapq

from wss.path import Path

# Direction map used for movement lookup (must match game DIRECTION_MAP)
DIRECTION_VECTORS = {
    "MoveNorth":     (0, -1),
    "MoveSouth":     (0, 1),
    "MoveEast":      (1, 0),
    "MoveWest":      (-1, 0),
    "MoveNorthEast": (1, -1),
    "MoveNorthWest": (-1, -1),
    "MoveSouthEast": (1, 1),
    "MoveSouthWest": (-1, 1),
}


class Brain:
    def make_move(self, player, game_map):
        raise NotImplementedError

    def decide_trade(self, trader, player, game_map):
        return trader.default_offer()

    def _can_move(self, path: Path, player, game_map) -> bool:
        """
        Check if the player can afford the first step of the path.
        """
        if not path or not path.directions:
            return False
        direction = path.directions[0]
        vec = DIRECTION_VECTORS.get(direction)
        if not vec:
            return False
        x, y = player.location
        nx, ny = x + vec[0], y + vec[1]
        sq = game_map.get_square(nx, ny)
        if not sq:
            return False
        t = sq.terrain

        return (
                player.current_strength >= t.move_cost and
                player.current_food >= t.food_cost and
                player.current_water >= t.water_cost
        )


class SurvivalBrain(Brain):
    # standard critical thinking brain focused on survival
    def make_move(self, player, game_map):
        print("\n[SurvivalBrain] Evaluating best move...")

        # Step 1: If strength is critically low → rest
        if player.current_strength <= 2:
            print("Low strength — resting.")
            return "rest"

        # Step 2: Seek water if hydration is low
        if player.current_water <= 3:
            print("Seeking water — hydration low.")
            path = player.vision.closest_water(game_map, player)
            self._print_path_info("Water", path)
            if path and self._can_move(path, player, game_map):
                return path.directions[0]

        # Step 3: Seek food if nutrition is low
        if player.current_food <= 3:
            print("Seeking food — nutrition low.")
            path = player.vision.closest_food(game_map, player)
            self._print_path_info("Food", path)
            if path and self._can_move(path, player, game_map):
                return path.directions[0]

        # Step 4: Progress eastward if resources are okay
        path = player.vision.easiest_path(game_map, player)
        self._print_path_info("Easiest Path", path)
        if path and self._can_move(path, player, game_map):
            print("Proceeding eastward.")
            return path.directions[0]

        # Step 5: No viable or safe path — rest
        print("No affordable path — resting.")
        return "rest"

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")


class RiskyBrain(Brain):
    # brain risks everything to move east indefinitely
    def make_move(self, player, game_map):
        print("\n[RiskyBrain] Charging forward no matter what!")

        # Step 1: If literally dying, rest
        if player.current_strength <= 0:
            print("Zero strength — forced rest.")
            return "rest"

        # Step 2: Stop only if you're out of food or water
        if player.current_food == 0 or player.current_water == 0:
            print("Critical starvation/dehydration — emergency rest.")
            return "rest"

        # Step 3: Always try to move east
        path = player.vision.easiest_path(game_map, player)
        self._print_path_info("Easiest Path", path)
        if self._can_move(path, player, game_map):
            print("Advancing east despite risks.")
            return path.directions[0]

        # Step 4: No path? Rest
        print("No known path — resting.")
        return "rest"

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")


class ResourceBrain(Brain):
    # Strategy focused on collecting resources before moving east
    def make_move(self, player, game_map):
        # Urgent water
        if player.current_water <= 2:
            print("Urgent need: water.")
            path = player.vision.closest_water(game_map, player)
            if self._can_move(path, player, game_map):
                return path.directions[0]

        # Urgent food
        if player.current_food <= 2:
            print("Urgent need: food")
            path = player.vision.closest_food(game_map, player)
            if self._can_move(path, player, game_map):
                return path.directions[0]

        # Rest if low strength
        if player.current_strength <= 3:
            print("Low strength - resting")
            return "rest"

        # Refill water if below threshold
        if player.current_water < player.max_water * 0.7:
            print("seeking water - below 70%")
            path = player.vision.closest_water(game_map, player)
            if self._can_move(path, player, game_map):
                return path.directions[0]

        # Refill food if below threshold
        if player.current_food < player.max_food * 0.7:
            print("seeking food - below 70%")
            path = player.vision.closest_food(game_map, player)
            if self._can_move(path, player, game_map):
                return path.directions[0]

        # collect nearby gold
        path = player.vision.closest_gold(game_map, player)
        if self._can_move(path, player, game_map):
            print("Collecting nearby gold.")
            return path.directions[0]

        # visit trader if affordable
        if player.current_food > 3 and player.current_water > 3:
            path = player.vision.closest_trader(game_map, player)
            if self._can_move(path, player, game_map):
                return path.directions[0]

        # default: move east
        print("Default: moving east")
        path = player.vision.easiest_path(game_map, player)
        if self._can_move(path, player, game_map):
            return path.directions[0]

        # fallback
        return "rest"

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")
