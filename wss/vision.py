# vision.py
# Player sight and scanning surrounding squares

from wss.path import Path

class Vision:
    """Base Vision class for looking at neighboring squares"""

    def get_visible_squares(self, game_map, player):
        """Returns a list of visible square coordinates - implemented by subclasses"""
        raise NotImplementedError

    def _find_paths_with_condition(self, game_map, player, condition_func):
        """Generic method to find paths based on a condition function"""
        paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and condition_func(square):
                path = self._create_path_to(player.location, coords)
                if path:
                    paths.append(path)

        if not paths:
            return []

        # Sort paths by distance, then movement cost, then eastward position
        paths.sort(key=lambda p: (
            len(p.directions),
            p.total_cost()['movement'],
            -p.end_position[0]  # Negative to prioritize eastward positions
        ))

        return paths

    def closest_food(self, game_map, player):
        """Find the closest square with food bonus"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_food_bonus())
        return paths[0] if paths else None

    def closest_water(self, game_map, player):
        """Find the closest square with water bonus"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_water_bonus())
        return paths[0] if paths else None

    def second_closest_food(self, game_map, player):
        """Find the second closest square with food"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_food_bonus())
        return paths[1] if len(paths) >= 2 else None

    def second_closest_water(self, game_map, player):
        """Find the second closest square with water bonus"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_water_bonus())
        return paths[1] if len(paths) >= 2 else None

    def easiest_path(self, game_map, player):
        """Find the path with the lowest movement cost"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.is_passable())

        if not paths:
            return None

        # Re-sort by movement cost, then eastward position
        paths.sort(key=lambda p: (
            p.total_cost()['movement'],
            -p.end_position[0]
        ))

        return paths[0] if paths else None

    def closest_gold(self, game_map, player):
        """Find the closest square with gold bonus"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_gold_bonus())
        return paths[0] if paths else None

    def second_closest_gold(self, game_map, player):
        """Find the second closest square with gold bonus"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_gold_bonus())
        return paths[1] if len(paths) >= 2 else None

    def closest_trader(self, game_map, player):
        """Find the closest square with a trader"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_trader())
        return paths[0] if paths else None

    def second_closest_trader(self, game_map, player):
        """Find the second closest square with trader"""
        paths = self._find_paths_with_condition(game_map, player, lambda square: square.has_trader())
        return paths[1] if len(paths) >= 2 else None

    def find_path_to(self, game_map, player, target_pos):
        """Find a path to a specific position"""
        # Check if the target position is within vision range
        visible_squares = self.get_visible_squares(game_map, player)
        if target_pos not in visible_squares:
            return None

        # Check if the target square is passable
        target_square = game_map.get_square(target_pos[0], target_pos[1])
        if not target_square or not target_square.is_passable():
            return None

        # Create a path from current position to target position
        return self._create_path_to(player.location, target_pos)

    def _create_path_to(self, start_pos, end_pos):
        """Create a Path object from start position to end position"""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        direction = self._get_direction(dx, dy)
        if not direction:
            return None

        return Path(
            directions = [direction],
            start_position = start_pos,
            end_position = end_pos,
            movement_costs = [1],    # Placeholder
            food_costs = [0.5],      # Placeholder
            water_costs = [0.5]      # Placeholder
        )

    def _get_direction(self, dx, dy):
        """Convert a displacement vector to a direction string"""
        # Supports only cardinal directions: East, West, North, South
        # If both dx and dy are non-zero, prioritize dx (horizontal movement first)
        if dx > 0:
            return "Move-East"
        elif dx < 0:
            return "Move-West"
        elif dy < 0:  # Note: North is decreasing y, South is increasing y in this coordinate system
            return "Move-North"
        elif dy > 0:
            return "Move-South"
        return None


class CautiousVision(Vision):
    """Vision that sees North, South and East"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to CautiousVision"""
        x, y = player.location
        visible = [
            (x, y + 1),  # North
            (x, y - 1),  # South
            (x + 1, y),  # East
        ]
        return [coords for coords in visible if game_map.is_valid_position(coords)]


class FocusedVision(Vision):
    """Vision that sees only the East square"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to FocusedVision"""
        x, y = player.location
        visible = [
            (x + 1, y),  # East
        ]
        return [coords for coords in visible if game_map.is_valid_position(coords)]


class KeenEyed(Vision):
    """Vision that sees North, South, East, West, and second East"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to KeenEyed"""
        x, y = player.location
        visible = [
            (x, y - 1),  # North
            (x, y + 1),  # South
            (x + 1, y),  # East
            (x - 1, y),  # West
            (x + 2, y),  # Second East
        ]
        return [coords for coords in visible if game_map.is_valid_position(coords)]


class FarSight(Vision):
    """Vision that sees two tiles in all cardinal directions, and farther east"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to FarSight"""
        x, y = player.location
        visible = [
            # North
            (x, y - 1),
            (x, y - 2),

            # South
            (x, y + 1),
            (x, y + 2),

            # East
            (x + 1, y),
            (x + 2, y),

            # West
            (x - 1, y),
            (x - 2, y),

            # Extra distant East tiles
            (x + 3, y),
            (x + 4, y),
        ]
        return [coords for coords in visible if game_map.is_valid_position(coords)]

