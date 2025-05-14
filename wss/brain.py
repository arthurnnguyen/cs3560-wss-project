from wss.path import Path

class Brain:
    def make_move(self, player, game_map):
        # Base method to decide the next action
        raise NotImplementedError

    def suggest_move(self, game_map, player):
        # Suggest a direction for the player
        raise NotImplementedError


class SurvivalBrain(Brain):
    def make_move(self, player, game_map):
        # Survival strategy: prioritize water, food, rest when needed, and move eastward
        print("\n[SurvivalBrain] Evaluating best move...")

        # Step 1: Check player's critical condition
        if player.current_water <= 2:
            print("Urgent need: Water")
            path = player.vision.closest_water(game_map, player)
            self._print_path_info("Water", path)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        if player.current_food <= 2:
            print("Urgent need: Food")
            path = player.vision.closest_food(game_map, player)
            self._print_path_info("Food", path)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        # Step 2: If strength is too low
        if player.current_strength <= 2:
            print("Low strength — resting.")
            return "rest"

        # Step 3: Check if gold is nearby
        gold_path = player.vision.closest_gold(game_map, player)
        if gold_path and self.is_path_affordable(gold_path, player):
            print("Gold detected nearby!")
            self._print_path_info("Gold", gold_path)
            return gold_path.directions[0]

        # Step 4: Find trader if player has enough resources
        if player.current_food > 3 and player.current_water > 3:
            trader_path = player.vision.closest_trader(game_map, player)
            if trader_path and self.is_path_affordable(trader_path, player):
                print("Trader detected nearby!")
                self._print_path_info("Trader", trader_path)
                return trader_path.directions[0]

        # Step 5: Evaluate eastward progress (easiest path)
        path = player.vision.easiest_path(game_map, player)
        self._print_path_info("Easiest path", path)
        if path and self.is_path_affordable(path, player):
            print("Chose to move eastward.")
            return path.directions[0]

        # Step 6: No viable path — stay still
        print("No safe move — resting.")
        return "rest"

    def suggest_move(self, game_map, player):
        # Suggest direction based on survival strategy
        suggestions = {}

        # Check water
        if player.current_water <= 3:
            path = player.vision.closest_water(game_map, player)
            if path and len(path.directions) > 0:
                end_x, end_y = path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_water_bonus():
                    direction = self._convert_direction_to_key(path.directions[0])
                    if direction:
                        full_path = self._format_full_path(path)
                        suggestions[direction] = f"Water is low, find water at ({end_x}, {end_y}). Path: {full_path}"

        # Check food
        if player.current_food <= 3:
            path = player.vision.closest_food(game_map, player)
            if path and len(path.directions) > 0:
                end_x, end_y = path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_food_bonus():
                    direction = self._convert_direction_to_key(path.directions[0])
                    if direction and direction not in suggestions:
                        full_path = self._format_full_path(path)
                        suggestions[direction] = f"Food is low, find food at ({end_x}, {end_y}). Path: {full_path}"

        # Check strength
        if player.current_strength <= 3:
            suggestions["r"] = "Low strength, should rest to recover"

        # If resources are fine, look for any nearby resource
        if not suggestions and player.current_water > 3 and player.current_food > 3:
            visible_squares = player.vision.get_visible_squares(game_map, player)
            resource_found = False

            for square_pos in visible_squares:
                x, y = square_pos
                square = game_map.get_square(x, y)

                if square_pos == player.location:
                    continue

                if square and square.is_passable() and (
                    square.has_food_bonus() or
                    square.has_water_bonus() or
                    square.has_gold_bonus() or
                    square.has_trader()
                ):
                    path = player.vision.find_path_to(game_map, player, square_pos)

                    if path and len(path.directions) > 0 and self.is_path_affordable(path, player):
                        direction = self._convert_direction_to_key(path.directions[0])
                        if direction:
                            full_path = self._format_full_path(path)

                            if square.has_food_bonus():
                                reason = "food"
                            elif square.has_water_bonus():
                                reason = "water"
                            elif square.has_gold_bonus():
                                reason = "gold"
                            elif square.has_trader():
                                reason = "trader"

                            suggestions[direction] = f"Detected {reason} at direction {direction} position ({x}, {y}). Path: {full_path}"
                            resource_found = True
                            break

            # If no resource found, suggest moving eastward
            if not resource_found:
                player_x, player_y = player.location
                east_squares = [(x, y) for x, y in visible_squares if x > player_x and game_map.get_square(x, y).is_passable()]

                if east_squares:
                    east_squares.sort(key=lambda pos: abs(pos[0] - player_x) + abs(pos[1] - player_y))
                    target_pos = east_squares[0]
                    path = player.vision.find_path_to(game_map, player, target_pos)

                    if path and len(path.directions) > 0 and self.is_path_affordable(path, player):
                        direction = self._convert_direction_to_key(path.directions[0])
                        if direction:
                            full_path = self._format_full_path(path)
                            suggestions[direction] = f"Resources are sufficient, move east to ({target_pos[0]}, {target_pos[1]}). Path: {full_path}"

        return suggestions

    def _format_full_path(self, path):
        # Format full path by combining repeated directions
        if not path or not path.directions:
            return "No path"

        direction_names = {
            "Move-East": "East",
            "Move-West": "West",
            "Move-North": "North",
            "Move-South": "South"
        }

        direction_counts = {}
        for direction in path.directions:
            if direction in direction_names:
                en_direction = direction_names[direction]
                direction_counts[en_direction] = direction_counts.get(en_direction, 0) + 1
            else:
                direction_counts[direction] = 1

        path_str = []
        for direction, count in direction_counts.items():
            if count == 1:
                path_str.append(f"move {direction}")
            else:
                path_str.append(f"move {direction} {count} times")

        return ", ".join(path_str)

    def _convert_direction_to_key(self, direction):
        # Convert movement string to direction key
        direction_map = {
            "Move-East": "e",
            "Move-West": "w",
            "Move-North": "n",
            "Move-South": "s"
        }
        return direction_map.get(direction)

    def is_path_affordable(self, path, player):
        # Check if player has enough resources to follow the path
        cost = path.total_cost()
        print(f"Evaluating affordability — Cost: {cost}, Player stats: Strength={player.current_strength}, Food={player.current_food}, Water={player.current_water}")
        return (
            player.current_food >= cost['food']
            and player.current_water >= cost['water']
            and player.current_strength >= cost['movement']
        )

    def _print_path_info(self, label, path):
        # Print path info
        if path:
            print(f"\n[Path Info — {label}]")
            print(f"From {path.start_position} to {path.end_position}")
            print(f"Directions: {path.directions}")
            print(f"Total cost: {path.total_cost()}")
        else:
            print(f"[Path Info — {label}] No valid path found.")

class ResourceBrain(Brain):
    # Strategy focused on collecting resources before moving east
    def make_move(self, player, game_map):
        print("\n[ResourceBrain] Evaluating best move...")

        # Step 1: Check player's critical condition
        if player.current_water <= 2:
            print("Urgent need: Water")
            path = player.vision.closest_water(game_map, player)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        if player.current_food <= 2:
            print("Urgent need: Food")
            path = player.vision.closest_food(game_map, player)
            if path and self.is_path_affordable(path, player):
                return path.directions[0]

        # Step 2: If strength is too low
        if player.current_strength <= 3:
            print("Low strength — resting.")
            return "rest"

        # Step 3: Prioritize collecting more resources if below 70% max
        if player.current_water < player.max_water * 0.7:
            water_path = player.vision.closest_water(game_map, player)
            if water_path and self.is_path_affordable(water_path, player):
                print("Looking for more water...")
                return water_path.directions[0]

        if player.current_food < player.max_food * 0.7:
            food_path = player.vision.closest_food(game_map, player)
            if food_path and self.is_path_affordable(food_path, player):
                print("Looking for more food...")
                return food_path.directions[0]

        # Step 4: Find gold if resources are enough
        gold_path = player.vision.closest_gold(game_map, player)
        if gold_path and self.is_path_affordable(gold_path, player):
            print("Gold detected nearby!")
            return gold_path.directions[0]

        # Step 5: Find trader if player has enough resources
        if player.current_food > 3 and player.current_water > 3:
            trader_path = player.vision.closest_trader(game_map, player)
            if trader_path and self.is_path_affordable(trader_path, player):
                print("Trader detected nearby!")
                return trader_path.directions[0]

        # Step 6: Move eastward if resources are sufficient
        if player.current_food >= player.max_food * 0.5 and player.current_water >= player.max_water * 0.5:
            path = player.vision.easiest_path(game_map, player)
            if path and self.is_path_affordable(path, player):
                print("Chose to move eastward.")
                return path.directions[0]

        # Step 7: Rest to recover strength
        print("Resting to recover strength.")
        return "rest"

    def suggest_move(self, game_map, player):
        # Suggest direction based on resource-focused strategy
        suggestions = {}

        # Check critical danger conditions first
        if player.current_water <= 2:
            path = player.vision.closest_water(game_map, player)
            if path and len(path.directions) > 0:
                end_x, end_y = path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_water_bonus():
                    direction = self._convert_direction_to_key(path.directions[0])
                    if direction:
                        full_path = self._format_full_path(path)
                        suggestions[direction] = f"Water is critically low, find water at ({end_x}, {end_y}). Path: {full_path}"
                        return suggestions  # Highest priority

        if player.current_food <= 2:
            path = player.vision.closest_food(game_map, player)
            if path and len(path.directions) > 0:
                end_x, end_y = path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_food_bonus():
                    direction = self._convert_direction_to_key(path.directions[0])
                    if direction:
                        full_path = self._format_full_path(path)
                        suggestions[direction] = f"Food is critically low, find food at ({end_x}, {end_y}). Path: {full_path}"
                        return suggestions  # Highest priority

        # Check strength
        if player.current_strength <= 3:
            suggestions["r"] = "Low strength, should rest to recover"
            return suggestions  # High priority

        # Find gold if affordable
        gold_path = player.vision.closest_gold(game_map, player)
        if gold_path and self.is_path_affordable(gold_path, player):
            end_x, end_y = gold_path.end_position
            end_square = game_map.get_square(end_x, end_y)
            if end_square and end_square.has_gold_bonus():
                direction = self._convert_direction_to_key(gold_path.directions[0])
                if direction:
                    full_path = self._format_full_path(gold_path)
                    suggestions[direction] = f"Gold detected at ({end_x}, {end_y}), collect it. Path: {full_path}"

        # Find trader if affordable
        if player.current_food > 3 and player.current_water > 3:
            trader_path = player.vision.closest_trader(game_map, player)
            if trader_path and self.is_path_affordable(trader_path, player):
                end_x, end_y = trader_path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_trader():
                    direction = self._convert_direction_to_key(trader_path.directions[0])
                    if direction and direction not in suggestions:
                        full_path = self._format_full_path(trader_path)
                        suggestions[direction] = f"Trader detected at ({end_x}, {end_y}), consider trading. Path: {full_path}"

        # Replenish resources if under 70%
        if player.current_water < player.max_water * 0.7:
            water_path = player.vision.closest_water(game_map, player)
            if water_path and self.is_path_affordable(water_path, player):
                end_x, end_y = water_path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_water_bonus():
                    direction = self._convert_direction_to_key(water_path.directions[0])
                    if direction and direction not in suggestions:
                        full_path = self._format_full_path(water_path)
                        suggestions[direction] = f"Water below 70%, collect more at ({end_x}, {end_y}). Path: {full_path}"

        if player.current_food < player.max_food * 0.7:
            food_path = player.vision.closest_food(game_map, player)
            if food_path and self.is_path_affordable(food_path, player):
                end_x, end_y = food_path.end_position
                end_square = game_map.get_square(end_x, end_y)
                if end_square and end_square.has_food_bonus():
                    direction = self._convert_direction_to_key(food_path.directions[0])
                    if direction and direction not in suggestions:
                        full_path = self._format_full_path(food_path)
                        suggestions[direction] = f"Food below 70%, collect more at ({end_x}, {end_y}). Path: {full_path}"

        # Move east if resources are sufficient and nothing else urgent
        if not suggestions and player.current_food >= player.max_food * 0.5 and player.current_water >= player.max_water * 0.5:
            visible_squares = player.vision.get_visible_squares(game_map, player)
            resource_found = False

            for square_pos in visible_squares:
                x, y = square_pos
                square = game_map.get_square(x, y)

                if square_pos == player.location:
                    continue

                if square and square.is_passable() and (
                    square.has_food_bonus() or
                    square.has_water_bonus() or
                    square.has_gold_bonus() or
                    square.has_trader()
                ):
                    path = player.vision.find_path_to(game_map, player, square_pos)

                    if path and len(path.directions) > 0 and self.is_path_affordable(path, player):
                        direction = self._convert_direction_to_key(path.directions[0])
                        if direction:
                            full_path = self._format_full_path(path)

                            if square.has_food_bonus():
                                reason = "food"
                            elif square.has_water_bonus():
                                reason = "water"
                            elif square.has_gold_bonus():
                                reason = "gold"
                            elif square.has_trader():
                                reason = "trader"

                            suggestions[direction] = f"Detected {reason} at direction {direction} position ({x}, {y}). Path: {full_path}"
                            resource_found = True
                            break

            # If no resource found, suggest moving east
            if not resource_found:
                player_x, player_y = player.location
                east_squares = [(x, y) for x, y in visible_squares if x > player_x and game_map.get_square(x, y).is_passable()]
                if east_squares:
                    east_squares.sort(key=lambda pos: abs(pos[0] - player_x) + abs(pos[1] - player_y))
                    target_pos = east_squares[0]
                    path = player.vision.find_path_to(game_map, player, target_pos)
                    if path and len(path.directions) > 0 and self.is_path_affordable(path, player):
                        direction = self._convert_direction_to_key(path.directions[0])
                        if direction:
                            full_path = self._format_full_path(path)
                            suggestions[direction] = f"Resources sufficient, move east to ({target_pos[0]}, {target_pos[1]}). Path: {full_path}"

        # If no suggestion available, rest
        if not suggestions:
            suggestions["r"] = "No good path available, rest to recover strength"

        return suggestions

    def _format_full_path(self, path):
        # Format full path by combining repeated directions
        if not path or not path.directions:
            return "No path"

        direction_names = {
            "Move-East": "East",
            "Move-West": "West",
            "Move-North": "North",
            "Move-South": "South"
        }

        direction_counts = {}
        for direction in path.directions:
            if direction in direction_names:
                en_direction = direction_names[direction]
                direction_counts[en_direction] = direction_counts.get(en_direction, 0) + 1
            else:
                direction_counts[direction] = 1

        path_str = []
        for direction, count in direction_counts.items():
            if count == 1:
                path_str.append(f"move {direction}")
            else:
                path_str.append(f"move {direction} {count} times")

        return ", ".join(path_str)

    def _convert_direction_to_key(self, direction):
        # Convert movement string to direction key
        direction_map = {
            "Move-East": "e",
            "Move-West": "w",
            "Move-North": "n",
            "Move-South": "s"
        }
        return direction_map.get(direction)

    def is_path_affordable(self, path, player):
        # Check if player has enough resources to follow the path
        cost = path.total_cost()
        return (
            player.current_food >= cost['food']
            and player.current_water >= cost['water']
            and player.current_strength >= cost['movement']
        )
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
    
    def _convert_direction_to_key(self, direction):
        direction_map = {
        "Move-East": "e",
        "Move-West": "w",
        "Move-North": "n",
        "Move-South": "s"
    }
        return direction_map.get(direction)

    def _print_path_info(self, label, path):
        if path:
            print(f"\n[Path Info — {label}]")
            print(path)
        else:
            print(f"[Path Info — {label}] No valid path found.")

    def suggest_move(self, game_map, player):
        suggestions = {}

    # Suggest resting if player is out of strength, food, or water
        if player.current_strength <= 0:
            suggestions["r"] = "You're out of strength. Rest is mandatory."
            return suggestions

        if player.current_food == 0 or player.current_water == 0:
            suggestions["r"] = "You're out of food or water. Rest is required to survive."
            return suggestions

    # Try to move east if possible
        path = player.vision.easiest_path(game_map, player)
        if path and len(path.directions) > 0:
            direction = self._convert_direction_to_key(path.directions[0])
            if direction:
                suggestions[direction] = "RiskyBrain says: Keep going east, no matter what."
                return suggestions

    # If no path found, rest
        suggestions["r"] = "No path available. You should rest."
        return suggestions



