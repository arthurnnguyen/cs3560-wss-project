# brain.py
# Player decision making strategy

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


class SurvivalBrain(Brain):
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
            if path and self.is_path_affordable(path, player, game_map):
                return path.directions[0]

        # Step 3: Seek food if nutrition is low
        if player.current_food <= 3:
            print("Seeking food — nutrition low.")
            path = player.vision.closest_food(game_map, player)
            self._print_path_info("Food", path)
            if path and self.is_path_affordable(path, player, game_map):
                return path.directions[0]

        # Step 4: Progress eastward if resources are okay
        path = player.vision.easiest_path(game_map, player)
        self._print_path_info("Easiest Path", path)
        if path and self.is_path_affordable(path, player, game_map):
            print("Proceeding eastward.")
            return path.directions[0]

        # Step 5: No viable or safe path — rest
        print("No affordable path — resting.")
        return "rest"

    def is_path_affordable(self, path, player, game_map):
        if not path.directions:
            return False

        direction = path.directions[0]
        dx, dy = DIRECTION_VECTORS.get(direction, (0, 0))
        x, y = player.location
        next_square = game_map.get_square(x + dx, y + dy)
        if not next_square:
            return False

        t = next_square.terrain
        print(
            f"Evaluating next step affordability — Terrain: {t.name}, "
            f"Cost: strength={t.move_cost}, food={t.food_cost}, water={t.water_cost}, "
            f"Player: strength={player.current_strength}, food={player.current_food}, water={player.current_water}"
        )

        return (
            player.current_strength >= t.move_cost
            and player.current_food >= t.food_cost
            and player.current_water >= t.water_cost
        )

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")


class RiskyBrain(Brain):
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
        if path:
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