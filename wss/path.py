# path.py
# represents a movement path with cost summary

class Path:
    def __init__(self, directions, start_position, end_position, movement_costs, food_costs, water_costs):
        self.directions = directions
        self.start_position = start_position
        self.end_position = end_position
        self.movement_costs = movement_costs
        self.food_costs = food_costs
        self.water_costs = water_costs

    def total_cost(self):
        return {
            'movement': sum(self.movement_costs),
            'food': sum(self.food_costs),
            'water': sum(self.water_costs),
        }

    def __str__(self):
        return (
            f"Path from {self.start_position} to {self.end_position}\n"
        )
