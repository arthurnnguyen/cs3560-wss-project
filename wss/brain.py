# player decison making strategy
# brain.py

from wss.path import Path

class Brain:
    def make_move(self, player, game_map):
        raise NotImplementedError

class SurvivalBrain(Brain):
    def make_move(self, player, game_map):
        print("\n[SurvivalBrain] Evaluating best move...")

        # Step 1: Check player status (critical values)
        if player.current_water <= 2:
            print("Critical need: Water")
            path = player.vision.closest_water(game_map, player)
            self._print_path_info("Water", path)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        if player.current_food <= 2:
            print("Critical need: Food")
            path = player.vision.closest_food(game_map, player)
            self._print_path_info("Food", path)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        # Step 2: Check if strength is too low
        if player.current_strength <= 2:
            print("Low strength — resting.")
            return "rest"

        # Step 3: Evaluate progress toward east (easiest path)
        path = player.vision.easiest_path(game_map, player)
        self._print_path_info("Easiest Path", path)
        if path and self.is_path_affordable(path, player):
            print("Path to east selected.")
            return path.directions[0]

        # Step 4: No viable path — stay put
        print("No safe move — staying still.")
        return "rest"

    def is_path_affordable(self, path, player):
        cost = path.total_cost()
        print(f"Evaluating affordability — Cost: {cost}, Player Stats: "
              f"Strength={player.current_strength}, Food={player.current_food}, Water={player.current_water}")
        return (
            player.current_food >= cost['food']
            and player.current_water >= cost['water']
            and player.current_strength >= cost['movement']
        )

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")