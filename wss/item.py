
class Item: #modify player stats
    def apply_to(self, player):
        pass  


class FoodBonus(Item):
    def __init__(self, amount=5, is_repeating=False):
        super().__init__(is_repeating)
        self.amount = amount #how much food the player gets

    def apply_to(self, player): #increases amount wtout going over max
        player.current_food = min(player.max_food, player.current_food + self.amount)


class WaterBonus(Item):
    def __init__(self, amount=5, is_repeating=False):
        super().__init__(is_repeating)
        self.amount = amount

    def apply_to(self, player):
        player.current_water = min(player.max_water, player.current_water + self.amount)


class GoldBonus(Item):
    def __init__(self, amount=3):
        super().__init__(is_repeating=False)
        self.amount = amount

    def apply_to(self, player):
        player.current_gold += self.amount