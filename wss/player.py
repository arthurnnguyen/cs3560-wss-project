# player resource management and movement

class Player:
    def __init__(self, max_strength, max_water, max_food, vision, brain, location):
        self.max_strength = max_strength
        self.max_water = max_water
        self.max_food = max_food

        self.current_strength = max_strength
        self.current_water = max_water
        self.current_food = max_food
        self.current_gold = 0

        self.vision = vision
        self.brain = brain
        self.location = location  

    def move(self, direction, game_map):
        x, y = self.location
        dx, dy = direction
        new_x, new_y = x + dx, y + dy

        # 1. Boundary + existence check
        target = game_map.get_square(new_x, new_y)
        if not target:
            print("Move blocked: off the map.")
            return False

        # ← ADD THESE LINES
        t = target.terrain
        print(
            f"[DEBUG] Target terrain: {t.name} || costs: move={t.move_cost}, food={t.food_cost}, "
            f"water={t.water_cost}")
        print(
            f"[DEBUG] Your resources: strength={self.current_strength}, food={self.current_food}, "
            f"water={self.current_water}")
        # ← END DEBUG BLOCK

        # 2. Resource check
        if not self.can_enter(target):
            print("Move blocked: insufficient resources for", target.terrain.name)
            return False

        # 3. Deduct costs and update position
        self.apply_terrain_costs(target)
        self.location = (new_x, new_y)
        return True

    def can_enter(self, square):
        t = square.terrain
        return (
            self.current_strength >= t.move_cost and
            self.current_food >= t.food_cost and
            self.current_water >= t.water_cost
        )

    def apply_terrain_costs(self, square):
        t = square.terrain
        self.current_strength -= t.move_cost
        self.current_food -= t.food_cost
        self.current_water -= t.water_cost

    def collect(self, item):
        item.apply_to(self)

    def rest(self):
        self.current_strength = min(self.max_strength, self.current_strength + 2)
        self.current_food -= 0.5
        self.current_water -= 0.5

    def trade_with(self, trader):
        trader.initiate_trade(self)
