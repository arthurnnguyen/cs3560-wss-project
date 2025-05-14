from wss.map import Map
from wss.player import Player
from wss.brain import Brain

def setup_game():
    difficulty = input("Choose difficulty (easy, medium, hard): ")
    game_map = Map(width=10, height=10, difficulty=difficulty)
    brain = Brain()
    location = (0,0)
    player = Player(
    max_strength=10,
    max_water=5,
    max_food=5,
    vision=None,        # or whatever vision object your game expects
    brain=brain,
    location=location
)
    return game_map, player