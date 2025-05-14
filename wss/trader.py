import random

class Trader:

    # Constructor for trader
    def __init__(self):
        self.counterOfferCount = 0
        self.moodState = "good" # Starts in a 'good' mood for max of 5 chances at trades before reaching 'bad'

    # Start proccess for trading
    def initiate_trade(self, player):

        if(random.randint(0,100) <= 25):
            self.encounter(player) # 25% for an encounter with the strange Trader

        response = input("Trader: Hello! Would you like to trade? (y/n)\n")
        confirm = 0

        while(confirm == 0):    # Used to make sure response is entered correctly to start trading
            if(response.lower() == "y"):
                tradeType = input("Trader: Wonderful! What would you like to trade? (water/food)\n")
                confirm = 1
                self.respond_to_offer(tradeType, player)

            elif(response.lower() == "n"):
                print("Trader: Goodbye then, adventurer.")
                confirm = 1
                self.exit_trade()
            else:
                response = input("Trader: I'm sorry? Could you repeat that? (Please enter y or n)\n")

    # Trading looping and changes based off of the traders mood and amount of offers made
    def propose_trade(self, player, tradeType, itemAmount, goldAmount):

        if(self.counterOfferCount > 2 ):
            self.moodState = "moderate"

        elif(self.counterOfferCount > 4):
            self.moodState = "bad"

        self.counterOfferCount = self.counterOfferCount + 1

        if(self.moodState == "good"):   # Good mood means more items for less gold
            print("Trader: Would you consider this instead?")
            if(tradeType == "water"):
               itemAmount = (goldAmount / 2) + 1
               answer = input(f"{itemAmount} water for {goldAmount} gold?")
            elif(tradeType == "food"):
               itemAmount = (goldAmount / 3) + 1
               answer = input(f"{itemAmount} food for {goldAmount} gold?")
               if(answer == 'y'):
                  print("Trader: I accept your offer.")
                  player.food = player.food + itemAmount
                  player.gold = player.gold - goldAmount
                  self.exit_trade()
               elif(answer == 'n'):
                   self.propose_trade(player, tradeType, itemAmount, goldAmount)

        elif(self.moodState == "moderate"): # Moderate mood means items for their normal cost
            print("Trader: Not budging, huh? Alright.")
            if(tradeType == "water"):
               itemAmount = (goldAmount / 2)
               answer = input(f"{itemAmount} water for {goldAmount} gold?")
            elif(tradeType == "food"):
               itemAmount = (goldAmount / 3)
               answer = input(f"{itemAmount} food for {goldAmount} gold?")
               if(answer == 'y'):
                  print("Trader: I accept your offer.")
                  player.food = player.food + itemAmount
                  player.gold = player.gold - goldAmount
                  self.exit_trade()
               elif(answer == 'n'):
                   self.propose_trade(player, tradeType, itemAmount, goldAmount)

        elif(self.moodState == "bad"):  # Trader ends trading if mood reaches 'bad'
            print("Trader: There's just no pleasing you.")
            self.exit_trade()



    # Counter offer from Player
    def respond_to_offer(self, tradeType, player):

        if(tradeType == "water"):
            waterAmount = int(input("Trader: How much water would you like? (Enter a number)"))
            goldAmount = int(input("Trader: And how much are you willing to pay? (Enter a number)"))

            if(player.water >= waterAmount):
                if((goldAmount / waterAmount) < 2):
                    self.propose_trade(player, tradeType, waterAmount, goldAmount)
                elif(((goldAmount / waterAmount) >= 2)):
                    print("I accept your offer.")
                    player.water = player.water + waterAmount
                    player.gold = player.gold - goldAmount
                    self.exit_trade()
            else:   # To make sure the player doesn't trade what they don't have
                print("Trader: Are you trying to fool me? (You either do not have the proper amount of water(" + player.water + ") or gold ("
                       + player.gold + "). Please try again.")
                self.respond_to_offer(self, tradeType, player)

        if(tradeType == "food"):
            foodAmount = int(input("Trader: How much food would you like? (Enter a number)"))
            goldAmount = int(input("Trader: And how much are you willing to pay? (Enter a number)"))

            if(player.food >= foodAmount):
                if((goldAmount / foodAmount) < 3):
                    self.propose_trade(player, tradeType, foodAmount, goldAmount)
                elif(((goldAmount / foodAmount) >= 3)):
                    print("Trader: I accept your offer.")
                    player.food = player.food + foodAmount
                    player.gold = player.gold - goldAmount
                    self.exit_trade()
            else:
                print("Trader: Are you trying to fool me? (You either do not have the proper amount of food(" + player.food + ") or gold ("
                       + player.gold + "). Please try again.")
                self.respond_to_offer(self, tradeType, player)

    # The player has a chance to encounter this trader that has some different items for sale
    def encounter(self, player):
        print("You encounter a strange looking man in a long, torn-up coat.")
        response = input("Trader(?): Hello, stranger. Would you like to take a look and my wares? (y/n)")

        # The options are the same, with some good and some bad, and a 50/50 chance for good or bad on a specifc item
        if(response.lower() == "y"):
             print("(Please input the number of the item you would like to purchase, or 4 to leave interaction. Items will be consumed automatically.)\n")
             choice = input("[1] Mystery Meat(8g) - Should meat be that color? \n" \
             "[2] Odd Potion(5g) - There is nothing to suggest what this will do to you. \n" \
             "[3] Poison Vial(1g) - You have no use for this\n"
             "[4] Leave Encounter.\n")

             if(choice == 1):
                 print("Trader(?): Glad to do buissness with you.")
                 player.food = player.food + 10
                 player.gold = player.gold - 8
                 print("The meat had a pleasnt taste despite its...appearence. (+10 food)")
                 self.exit_trade()

             elif(choice == 2):
                 print("Trader(?): Careful with your choices, stranger.")
                 event = random.randint(0, 100)

                 if(event <= 50 ):
                     player.water = player.water + 10
                     player.gold = player.gold - 5
                     print("Strangly refreshing. (+10 water)")
                     self.exit_trade()
                 elif(event < 50 ):
                     player.water = player.water - 5
                     player.gold = player.gold - 5
                     print("That tasted absolulety horrible. (-5 water)")
                     self.exit_trade()

             elif(choice == 3):
                 print("Trader(?): ...You do know this is posion, right? 'You nod.' Your funeral.")
                 print("Why would you buy this?? (Seriously, the instructions say 'consumed automatically'.)")
                 player.gold = player.gold - 1
                 player.strength = 0
                 self.exit_trade()

             elif(choice == 4):
                 print("Trader(?): Suit yourself, then.")
                 self.exit_trade()

        elif(response.lower() == "n"):
            print("Trader(?): Nice meeting you then. Farewell.")
            self.exit_trade()
            

    # Leave trading
    def exit_trade(self):
        return 0

