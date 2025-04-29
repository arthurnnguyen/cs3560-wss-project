# player.py

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

    def move(self, direction):
        x, y = self.location
        dx, dy = direction
        self.location = (x + dx, y + dy)

    def collect(self, item):
        item.apply_to(self)

    def rest(self):
        self.current_strength = min(self.max_strength, self.current_strength + 2)
        self.current_food -= 0.5
        self.current_water -= 0.5

    def trade_with(self, trader):
        trader.initiate_trade(self)