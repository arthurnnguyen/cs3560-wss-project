# trader.py

from wss.item import Item

class Trader(Item):
    def __init__(self):
        self.mood_state = "neutral"
        self.counter_offer_count = 0

    def initiate_trade(self, player):
        print("\nTrader: I have an offer for you.")
        print("Give me 2 food and 1 water, and I’ll give you 3 gold.")

        decision = input("Do you accept the offer? (y/n): ").strip().lower()

        if decision == 'y':
            if player.current_food >= 2 and player.current_water >= 1:
                player.current_food -= 2
                player.current_water -= 1
                player.current_gold += 3
                print("Trade accepted! You gave 2 food and 1 water, and got 3 gold.")
            else:
                print("You don’t have enough resources for this trade.")
        elif decision == 'n':
            self.counter_offer(player)
        else:
            print("Invalid input. Trader walks away.")

    def counter_offer(self, player):
        self.counter_offer_count += 1

        if self.counter_offer_count > 1:
            print("Trader: Too many counteroffers. I'm leaving.")
            return

        print("Trader: Fine. I’ll take just 1 food and 1 water for 2 gold.")
        decision = input("Do you accept this counteroffer? (y/n): ").strip().lower()

        if decision == 'y':
            if player.current_food >= 1 and player.current_water >= 1:
                player.current_food -= 1
                player.current_water -= 1
                player.current_gold += 2
                print("Trade accepted! You gave 1 food and 1 water, and got 2 gold.")
            else:
                print("You don’t have enough resources.")
        else:
            print("Trader: Deal’s off.")