# player sight and scanning surrounding squares
# vision.py
from wss.path import Path

class Vision:
    """Base Vision class for looking at neighboring squares"""

    def get_visible_squares(self, game_map, player):
        """Returns a list of visible square coordinates - implemented by subclasses"""
        raise NotImplementedError

    def closest_food(self, game_map, player):
        """Find the closest square with food bonus"""
        food_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    food_paths.append(path)
        
        if not food_paths:
            return None # no food found
        
        # sort paths by distance, then movement cost, then eastward position
        food_paths.sort(key=lambda p: (
            len(p.directions),
            p.total_cost()['movement'],
            -p.end_position[0] # negative to prioritize eastward positions
        ))

        return food_paths[0] if food_paths else None

    def closest_water(self, game_map, player):
        """Find the closest square with water bonus"""
        water_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_water_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    water_paths.append(path)
        
        if not water_paths:
            return None # no water found
        
        # sort paths by distance, then movement cost, then eastward position
        water_paths.sort(key=lambda p: (
            len(p.directions),
            p.total_cost()['movement'],
            -p.end_position[0] # negative to prioritize eastward positions
        ))

        return water_paths[0] if water_paths else None

    def second_closest_food(self, game_map, player):
        """Find the second closest square with food"""
        food_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    food_paths.append(path)

        if len(food_paths) < 2:
            return None # not enough food sources found
        

    def second_closest_water(self, game_map, player):
        """Find the second closest square with water bonus"""
        water_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    water_paths.append(path)

        if len(water_paths) < 2:
            return None # not enough water sources found

    def easiest_path(self, game_map, player):
        """Find the path with the lowest movement cost"""
        paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.is_passable():
                path = self._create_path_to(player.location, coords)
                if path:
                    paths.append(path)
        
        if not paths:
            return None # No viable paths
        
        # Sort by movement cost, then eastward position
        paths.sort(key=lambda p: (
            p.total_cost()['movement'],
            -p.end_position[0] # Negative to prioritize eastward position
        ))

        return paths[0] if paths else None

    def closest_gold(self, game_map, player):
        """Find the closest square with gold bonus"""
        gold_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    gold_paths.append(path)
        
        if not gold_paths:
            return None # no gold found
        
        # sort paths by distance, then movement cost, then eastward position
        gold_paths.sort(key=lambda p: (
            len(p.directions),
            p.total_cost()['movement'],
            -p.end_position[0] # negative to prioritize eastward positions
        ))

        return gold_paths[0] if gold_paths else None
    
    def second_closest_gold(self, game_map, player):
        """Find the second closest square with gold bonus"""
        gold_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    gold_paths.append(path)

        if len(gold_paths) < 2:
            return None # not enough gold sources found

    def closest_trader(self, game_map, player):
        """Find the closest square with a trader"""
        trader_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    trader_paths.append(path)
        
        if not trader_paths:
            return None # no trader found
        
        # sort paths by distance, then movement cost, then eastward position
        trader_paths.sort(key=lambda p: (
            len(p.directions),
            p.total_cost()['movement'],
            -p.end_position[0] # negative to prioritize eastward positions
        ))

        return trader_paths[0] if trader_paths else None

    def second_closest_trader(self, game_map, player):
        """Find the second closest square with trader"""
        trader_paths = []

        for coords in self.get_visible_squares(game_map, player):
            square = game_map.get_square(*coords)
            if square and square.has_food_bonus():
                path = self._create_path_to(player.location, coords)
                if path:
                    trader_paths.append(path)

        if len(trader_paths) < 2:
            return None # not enough traders found
        
    def _create_path_to(self, start_pos, end_pos):
        """Create a Path object from start position to end position"""
        # calculate the direction vector
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]

        # convert to a direction
        direction = self._get_direction(dx, dy)
        if not direction:
            return None
        
        # create and return the path with costs
        # use placeholder costs for now until map is fully implemented
        return Path(
            directions = [direction],
            start_position = start_pos,
            end_position = end_pos,
            movement_costs = [1], # Placeholder
            food_costs = [0.5], # Placeholder
            water_costs = [0.5] # Placeholder
        )
    
    def _get_direction(self, dx, dy):
        """Convert a displacement vector to a direction string"""
        direction_map = {
            (1, 0): "MoveEast",
            (-1, 0): "MoveWest",
            (0, 1): "MoveNorth",
            (0, -1): "MoveSouth",
            (1, 1): "MoveNorthEast",
            (-1, 1): "MoveNorthWest",
            (1, -1): "MoveSouthEast",
            (-1, -1): "MoveSouthWest",
        }  
        return direction_map.get((dx, dy), None)  
    
class CautiousVision(Vision):
    """Vision subclass that can only see North, South and East"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to CautiousVision"""
        x, y = player.location
        visible = [
            (x, y + 1), # North
            (x, y - 1), # South
            (x + 1, y), # East
        ]
        # Filter out squares that are outside map boundaries
        return [coords for coords in visible if game_map.is_valid_position(coords)]
    
class FocusedVision(Vision):
    """Vision subclass that can see East, NorthEast, and SouthEast squares"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to FocusedVision"""
        x, y = player.location
        visible = [
            (x + 1, y + 1), # NorthEast
            (x + 1, y - 1), # SouthEast
            (x + 1, y), # East
        ]
        # Filter out squares that are outside map boundaries
        return [coords for coords in visible if game_map.is_valid_position(coords)]
    
class KeenEyed(Vision):
    """Vision subclass that can see: North, South, NorthEast, East, SouthEast, Second East Square"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to FocusedVision"""
        x, y = player.location
        visible = [
            (x, y + 1), # North
            (x, y - 1), # South
            (x + 1, y + 1), # NorthEast
            (x + 1, y - 1), # SouthEast
            (x + 1, y), # East
            (x + 2, y), # Second East square
        ]
        # Filter out squares that are outside map boundaries
        return [coords for coords in visible if game_map.is_valid_position(coords)]
    
class FarSight(Vision):
    """Vision subclass that can see two squares out in every direction"""

    def get_visible_squares(self, game_map, player):
        """Returns coordinates of squares visible to FocusedVision"""
        x, y = player.location
        visible = [
            (x, y + 1), # North
            (x, y + 2), # Second North square
            (x, y - 1), # South
            (x, y - 2), # Second South square
            (x + 1, y + 1), # NorthEast
            (x + 1, y + 2), # NorthEast and North one square
            (x + 1, y - 1), # SouthEast
            (x + 1, y - 2), # SouthEast and South one square
            (x + 1, y), # East
            (x + 2, y - 1) # SouthEast and East one square
            (x + 2, y + 1) # NorthEast and East one square
            (x + 2, y), # Second East square
        ]
        # Filter out squares that are outside map boundaries
        return [coords for coords in visible if game_map.is_valid_position(coords)]

