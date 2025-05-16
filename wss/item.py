# bonuses like food, water, gold

# modify player stats
class Item:
    def __init__(self, repeating=False):
        self.repeating = repeating
        self.last_collected_turn = -1   # Initialize to an invalid turn number

    def can_collect(self, current_turn):
        return self.repeating and current_turn != self.last_collected_turn

    def apply_to(self, player, current_turn):
        # If non-repeating and already used, never apply.
        if not self.repeating and self.last_collected_turn is not None:
            return False

        # If repeating but already collected this turn, skip.
        if self.repeating and self.last_collected_turn == current_turn:
            return False

        # Delegate to subclass to actually modify player.
        applied = self._apply(player)
        if applied:
            self.last_collected_turn = current_turn
        return applied


    def _apply(self, player):
        # Subclasses override this to do the actual effect and return True.
        raise NotImplementedError


class FoodBonus(Item):
    def __init__(self, amount=5, repeating=False):
        super().__init__(repeating)
        self.amount = amount    # how much food the player gets

    def __str__(self):
        return f"FoodBonus(+{self.amount} food)"

    def apply_to(self, player, current_turn):     # increases amount without going over max
        before = player.current_food
        player.current_food = min(player.max_food, player.current_food + self.amount)
        return player.current_food > before


class WaterBonus(Item):
    def __init__(self, amount=5, repeating=False):
        super().__init__(repeating)
        self.amount = amount

    def __str__(self):
        return f"WaterBonus(+{self.amount} water)"

    def apply_to(self, player, current_turn):  # increases amount without going over max
        before = player.current_food
        player.current_food = min(player.max_food, player.current_food + self.amount)
        return player.current_food > before

class GoldBonus(Item):
    def __init__(self, amount=5, repeating=False):
        super().__init__(repeating)
        self.amount = amount

    def __str__(self):
        return f"GoldBonus(+{self.amount} gold)"

    def apply_to(self, player, current_turn):
        player.current_gold += self.amount
        return True
