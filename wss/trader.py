# wss/trader.py
# Automated Trader logic without user prompts, suitable for AI-driven trades
from .item import Item


class Trader(Item):
    def __init__(self, profile="generic", repeating=True):
        super().__init__(repeating=repeating)
        self.counter_offer_count = 0
        self.profile = profile

    def default_offer(self):
        # Returns the initial trade proposal as a tuple:
        #  ({resource: amount, ...}, {resource: amount, ...})
        # First dict is what trader wants, second is what trader gives.
        return {'food': 2, 'water': 1}, {'gold': 3}

    def counter_offer(self, previous_offer):

        # Generate a counteroffer (offer, request) or None to end trading.
        # Different logic for each profile:
        #   - Generous: up to 3 sweetening offers
        #   - Stingy: up to 2 minor concessions
        # Then mood-based fallback for 'moderate' or 'bad'.

        self.counter_offer_count += 1

        # GenerousTrader concessions
        if self.profile == "generous":
            if self.counter_offer_count <= 3:
                # sweet deal for player
                give = {'food': 1, 'water': 2}
                receive = {'gold': 1}
                return (give, receive)
            # after 3 counters, shift mood
            self.profile = "moderate"

        # StingyTrader concessions
        if self.profile == "stingy":
            if self.counter_offer_count <= 2:
                # small concession: one less food
                give = {'food': previous_offer[0]['food'] - 1, 'water': previous_offer[0]['water']}
                receive = {'gold': previous_offer[1]['gold']}
                return (give, receive)
            # after 2 counters, shift mood
            self.profile = "moderate"

        # Moderate mood (after initial concessions)
        if self.profile == "moderate":
            give = {'food': 1, 'water': 0}
            receive = {'gold': 1}
            # one moderate counter, then become 'bad'
            if self.counter_offer_count > (3 if previous_offer[0]['food'] < 2 else 1):
                self.profile = "bad"
            return (give, receive)

        # Bad mood: no further trades
        return None

    def initiate_trade(self, player, current_turn=None, game_map=None):
        print(f"\n--- Negotiation with {self.profile.title()}Trader ---")
        print(f"Player pre-trade resources: Str={player.current_strength}, "
              f"Food={player.current_food}, Water={player.current_water}, Gold={player.current_gold}")

        offer, request = self.default_offer()
        round = 0

        while True:
            round += 1
            print(f"[Round {round}] Trader offers {offer}  →  Player would receive {request}")

            # ask the brain how to respond
            choice_offer, choice_request = player.brain.decide_trade(self, player, game_map)
            if choice_offer is None:
                print("Player declines to negotiate further.")
                return False

            # if choice matches the trader’s current proposal, accept it
            if choice_offer == offer and choice_request == request:
                # check affordability
                if any(getattr(player, f"current_{res}") < amt for res, amt in offer.items()):
                    print("Player can't afford that offer; trade cancelled.")
                    return False

                # execute the swap
                for res, amt in offer.items():
                    setattr(player, f"current_{res}", getattr(player, f"current_{res}") - amt)
                for res, amt in request.items():
                    setattr(player, f"current_{res}", getattr(player, f"current_{res}") + amt)

                print("Trade accepted!")
                print(f"Post-trade resources: Str={player.current_strength}, "
                      f"Food={player.current_food}, Water={player.current_water}, Gold={player.current_gold}")
                return True

            # otherwise, generate a counter-offer
            counter = self.counter_offer((offer, request))
            if not counter:
                print("Trader is offended by haggling and walks away.")
                return False

            offer, request = counter
            print(f"Trader counters with {offer} → {request}")


class GenerousTrader(Trader):
    def __init__(self):
        super().__init__(profile="generous")

class StingyTrader(Trader):
    def __init__(self):
        super().__init__(profile="stingy")


class FoodTrader(Trader):
    """Offers food in exchange for some resources."""
    def __init__(self):
        super().__init__(profile="food")
    def default_offer(self):
        # want 2 gold, give 5 food
        return ({'gold': 2}, {'food': 5})
    def counter_offer(self, previous):
        # e.g. on counter, still want 2 gold, but give 7 food
        return ({'gold': 2}, {'food': 7})

class WaterTrader(Trader):
    """Offers water in exchange for some resources."""
    def __init__(self):
        super().__init__(profile="water")
    def default_offer(self):
        # want 1 gold, give 5 water
        return ({'gold': 1}, {'water': 3})
    def counter_offer(self, previous):
        return ({'gold': 1}, {'water': 5})