# Wilderness Survival System (WSS)

## Introduction

The Wilderness Survival System (WSS) is a simulation game where the player attempts to travel from the west to the east side of the map. Along the way, the player will encounter various terrain types, as well as dangers and resources like food, water, and gold.

## How to Play
	•	The player starts on the west side of the map and must move eastward.
	•	Each terrain type has different movement costs (strength, food, water).
	•	The player must collect and manage resources efficiently.
	•	The player can trade with traders to exchange resources.

## Main Components

### Map
	•	A grid of squares with various terrain types.
	•	Each square may contain items or a trader.
	•	The map size is customizable.

### Player
	•	Has stats: strength, water, food, and gold.
	•	Has two special components: Vision and Brain.

### Vision

There are 4 types of vision:
	1.	**Focused**: Only sees squares to the east.
	2.	**Cautious**: Sees squares to the north, south, and east.
	3.	**Keen-Eyed**: Sees more squares, including the second east square.
	4.	**Far-Sight**: Sees two squares in every cardinal direction.

Each vision type provides methods to find paths:
	•	closest_food: Finds the nearest food.
	•	closest_water: Finds the nearest water.
	•	closest_gold: Finds the nearest gold.
	•	closest_trader: Finds the nearest trader.
	•	second_closest_food, second_closest_water, etc.: Finds the second nearest resource.
	•	easiest_path: Finds the path with the lowest movement cost.

### Brain

There are 2 types of brain strategies:
	1.	**SurvivalBrain**: Prioritizes survival by finding food and water when needed.
	2.	**ResourceBrain**: Focuses on collecting resources before moving east.
  3.  **RiskyBrain**: 

### Terrain

Different terrain types with varying movement costs:
	•	**Plains**: Low cost.
	•	**Forest**: Medium cost.
	•	**Swamp**: High cost.
	•	**Mountain**: High movement cost, low water cost.

### Items
	•	Food: Increases food level.
	•	Water: Increases water level.
	•	Gold: Increases gold count.
	•	Trader: Allows trading resources.

## How to Run the Game
	1.	Run the main.py file to start the game in the terminal.
	2.	Run the wss/ui.py file to start the game with a graphical user interface.

## Controls
	•	Use the arrow keys to move.
	•	Press R to rest.
	•	Press I to view path information.
