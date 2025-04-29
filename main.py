# main.py

from wss.player import Player
from wss.item import FoodBonus, WaterBonus, GoldBonus
from wss.trader import Trader

if __name__ == "__main__":
    # dummy player
    player = Player(
        max_strength=10,
        max_water=10,
        max_food=10,
        vision=None,
        brain=None,
        location=(0, 0)
    )

    from wss.trader import Trader

trader = Trader()

trader.initiate_trade(player)

#stats after trade
print("\nAfter interaction:")
print(f"Food: {player.current_food}")
print(f"Water: {player.current_water}")
print(f"Gold: {player.current_gold}")