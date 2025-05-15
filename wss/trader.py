# wss/trader.py
# Automated Trader logic without user prompts, suitable for AI-driven trades
from .item import Item


class Trader(Item):
    def __init__(self):
        super().__init__(repeating=True)
        self.counter_offer_count = 0
        self.mood_state = "good"

    def default_offer(self):
        # Returns the initial trade proposal as a tuple:
        #  ({resource: amount, ...}, {resource: amount, ...})
        # First dict is what trader wants, second is what trader gives.
        return {'food': 2, 'water': 1}, {'gold': 3}

    def counter_offer(self, previous_offer):
        # Generate a counteroffer based on trader's mood and offer history.
        # Returns a new (offer, request) tuple or None to end trading.
        self.counter_offer_count += 1
        # Simple mood shift logic
        if self.counter_offer_count > 4:
            self.mood_state = "bad"
        elif self.counter_offer_count > 2:
            self.mood_state = "moderate"

        if self.mood_state == "good":
            # Better deal for player on first counters
            give = {'food': 1, 'water': 1}
            receive = {'gold': 2}
            return give, receive
        elif self.mood_state == "moderate":
            # Fair deal in moderate mood
            give = {'food': 1, 'water': 0}
            receive = {'gold': 1}
            return give, receive
        else:
            # Bad mood: no more trading
            return None

    def initiate_trade(self, player, current_turn=None, game_map=None):
        # Conducts a trade using the player's Brain.decide_trade logic.
        # Returns True if a trade occurred, False otherwise.

        # Get initial offer from trader
        offer, request = self.default_offer()

        # Ask the Brain what to do
        offer, request = player.brain.decide_trade(self, player, game_map)

        # If brain declines (None), exit
        if offer is None:
            return False

        print(f"Trader offers {offer} for {request}")

        # Check player can give resources
        if (player.current_food < offer.get('food', 0) or player.current_water < offer.get('water', 0)
                or player.current_gold < offer.get('gold', 0)):
            print("Trader: you can't afford that. Trade cancelled.")
            return False

        # Execute trade: deduct offer from player
        player.current_food -= offer.get('food', 0)
        player.current_water -= offer.get('water', 0)
        player.current_gold -= offer.get('gold', 0)
        # Credit request to player
        player.current_food += request.get('food', 0)
        player.current_water += request.get('water', 0)
        player.current_gold += request.get('gold', 0)

        print("Trader: trade completed.")
        return True


class GenerousTrader(Trader):
    def default_offer(self):
        return {'food': 1, 'water': 1}, {'gold': 2}

    def counter_offer(self, previous_offer):
        # very generous: always give one more water until exhausted
        self.counter_offer_count += 1
        if self.counter_offer_count > 3:
            return None
        give = {'food': 1, 'water': 2}
        receive = {'gold': 1}
        return give, receive


class StingyTrader(Trader):
    def default_offer(self):
        return {'food': 3, 'water': 2}, {'gold': 1}

    def counter_offer(self, previous_offer):
        self.counter_offer_count += 1
        # becomes even stingier each time
        if self.counter_offer_count > 2:
            return None
        give = {'food': 4, 'water': 3}
        receive = {'gold': 2}
        return give, receive
