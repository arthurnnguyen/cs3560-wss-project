#item.py
# bonusese like food, water, gold

#modify player stats
class Item:
    def __init__(self, repeating = False):
        self.repeating = repeating
        self.last_collected_turn = -1   # Initialize to an invalid turn number

    def can_collect(self, current_turn):
        return self.repeating and current_turn != self.last_collected_turn

    def apply_to(self, player, current_turn):
        if self.can_collect(current_turn) or not self.repeating:
            self.last_collected_turn = current_turn



class FoodBonus(Item):
    def __init__(self, amount=5):
        self.amount = amount    # how much food the player gets

    def __str__(self):
        return f"FoodBonus(+{self.amount} food)"

    def apply_to(self, player):     # increases amount without going over max
        player.current_food = min(player.max_food, player.current_food + self.amount)


class WaterBonus(Item):
    def __init__(self, amount=5):
        self.amount = amount

    def __str__(self):
        return f"WaterBonus(+{self.amount} water)"

    def apply_to(self, player):
        player.current_water = min(player.max_water, player.current_water + self.amount)


class GoldBonus(Item):
    def __init__(self, amount=3):
        self.amount = amount

    def __str__(self):
        return f"GoldBonus(+{self.amount} gold)"

    def apply_to(self, player):
        player.current_gold += self.amount