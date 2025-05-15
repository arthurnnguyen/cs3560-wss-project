# main_pygame.py

import sys
import pygame

from wss.item import WaterBonus, FoodBonus, GoldBonus
from wss.map import Map
from wss.player import Player
from wss.trader import Trader
from wss.brain import SurvivalBrain, RiskyBrain, ResourceBrain
from wss.vision import CautiousVision, FocusedVision, KeenEyed, FarSight


# You can add more Brain subclasses to this dict as you implement them
BRAIN_CHOICES = {
    'survival': SurvivalBrain,
    'risky': RiskyBrain,
    'resource': ResourceBrain,
}

# Vision style options
VISION_CHOICES = {
    'cautious': CautiousVision,
    'focused': FocusedVision,
    'keen': KeenEyed,
    'far': FarSight,
}

# Convert Path direction strings into (dx, dy) vectors
DIRECTION_MAP = {
    "MoveNorth": (0, -1),
    "MoveSouth": (0, 1),
    "MoveEast": (1, 0),
    "MoveWest": (-1, 0),
    "MoveNorthEast": (1, -1),
    "MoveNorthWest": (-1, -1),
    "MoveSouthEast": (1, 1),
    "MoveSouthWest": (-1, 1),
}


def choose_option(prompt, options):
    keys = list(options.keys())
    while True:
        choice = input(f"{prompt} ({'/'.join(keys)}): ").strip().lower()
        if choice in options:
            return options[choice]()
        print(f"Invalid choice. Please select one of: {', '.join(keys)}.")


def select_settings():
    # 1) Map size
    while True:
        try:
            w = int(input("Map width (squares): ").strip())
            h = int(input("Map height (squares): ").strip())
            if w > 0 and h > 0:
                break
            print("Width and height must be positive integers.")
        except ValueError:
            print("Please enter valid integers.")
    # 2) Difficulty
    diffs = ('easy', 'medium', 'hard')
    while True:
        d = input("Select difficulty (easy, medium, hard): ").strip().lower()
        if d in diffs:
            break
        print(f"Invalid choice. Pick from: {', '.join(diffs)}.")
    # 3) Vision & Brain
    vision = choose_option("Select vision style", VISION_CHOICES)
    brain = choose_option("Select brain strategy", BRAIN_CHOICES)

    return w, h, d, vision, brain


CELL_SIZE = 48
STATS_PANEL_HEIGHT = 100   # extra space at bottom
FPS = 1  # AI moves per second


def draw_map(screen, game_map):
    colors = {
        'plains': (200, 200, 150),
        'forest': (34, 139, 34),
        'desert': (237, 201, 175),
        'swamp':  (47, 79, 47),
        'mountain': (139, 137, 137),
    }
    for y in range(game_map.height):
        for x in range(game_map.width):
            terrain = game_map.get_square(x, y).terrain.name
            col = colors.get(terrain, (180, 180, 180))
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, col, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)


def draw_items(screen, game_map):
    for y in range(game_map.height):
        for x in range(game_map.width):
            sq = game_map.get_square(x, y)
            cx = x*CELL_SIZE + CELL_SIZE//2
            cy = y*CELL_SIZE + CELL_SIZE//2

            # Draw water bonuses (blue)
            if any(isinstance(i, WaterBonus) for i in sq.items):
                pygame.draw.circle(screen, (64, 164, 223), (cx, cy), 6)

            # Draw food bonuses (green)
            if any(isinstance(i, FoodBonus) for i in sq.items):
                pygame.draw.circle(screen, (34, 139, 34), (cx, cy), 6)

            # Draw gold bonuses (yellow)
            if any(isinstance(i, GoldBonus) for i in sq.items):
                pygame.draw.circle(screen, (218, 165, 32), (cx, cy), 6)

            # Draw traders (purple)
            if any(isinstance(i, Trader) for i in sq.items):
                pygame.draw.circle(screen, (128, 0, 128), (cx, cy), 8)


def draw_player(screen, player):
    x, y = player.location
    pygame.draw.circle(screen, (220, 20, 60),
        (x*CELL_SIZE+CELL_SIZE//2, y*CELL_SIZE+CELL_SIZE//2), CELL_SIZE//3)


def draw_stats(screen, player, height, turn):
    font = pygame.font.SysFont(None, 24)
    lines = [
        f"Turn: {turn}",
        f"Strength: {player.current_strength}/{player.max_strength}",
        f"Food:     {player.current_food:.1f}/{player.max_food}",
        f"Water:   {player.current_water:.1f}/{player.max_water}",
        f"Gold:    {player.current_gold}",
    ]
    base_y = height*CELL_SIZE + 10   # start 10px into the stats panel
    for i, text in enumerate(lines):
        surf = font.render(text, True, (230, 230, 230))
        screen.blit(surf, (10, base_y + i*18))


def draw_stats_panel_background(screen, width, height):
    panel_rect = pygame.Rect(
        0, height*CELL_SIZE,
        width*CELL_SIZE, STATS_PANEL_HEIGHT
    )
    pygame.draw.rect(screen, (30, 30, 30), panel_rect)


def main():
    # 1) initial settings
    width, height, difficulty, vision, brain = select_settings()

    # 2) init map & player
    game_map = Map(width, height, difficulty)
    start_y = height//2
    player = Player(25, 25, 25, vision, brain, (0, start_y))

    # 3) pygame init
    pygame.init()
    screen = pygame.display.set_mode((
        width * CELL_SIZE,
        height * CELL_SIZE + STATS_PANEL_HEIGHT
    ))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Wilderness Survival AI")

    turn = 1
    running = True
    result = None

    while running:
        # --- handle quit only ---
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        x, y = player.location
        square = game_map.get_square(x, y)

        # --- AI step ---
        if not result:
            # collect/trade
            sq = game_map.get_square(*player.location)
            for item in sq.items[:]:
                if isinstance(item, Trader):
                    player.trade_with(item, turn)
                else:
                    applied = item.apply_to(player, turn)
                    if applied and not item.repeating:
                        sq.remove_item(item)

            # Status
            print(f"\nTurn {turn}: Location {player.location} on {square.terrain.name}")
            print(f"Stats -> Strength: {player.current_strength}, Food: {player.current_food}, "
                  f"Water: {player.current_water}, Gold: {player.current_gold}")

            # check win/lose
            if player.location[0] >= width - 1:
                result = "YOU WIN!"
                print("PLAYER WON: reached east edge!")
            elif player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
                result = "GAME OVER"
                print("PLAYER FAILED: resources depleted.")
                print("GAME OVER!")

            if not result:
                action = player.brain.make_move(player, game_map)
                print(f"Player action: {action}")
                if action == 'rest':
                    player.rest()
                else:
                    vec = DIRECTION_MAP.get(action)
                    if vec and player.move(vec, game_map):
                        pass
                    else:
                        player.rest()
                turn += 1

        # --- draw everything ---
        screen.fill((0, 0, 0))
        draw_map(screen, game_map)
        draw_items(screen, game_map)
        draw_player(screen, player)
        # draw the stats panel
        draw_stats_panel_background(screen, width, height)
        draw_stats(screen, player, height, turn)

        # if game over, overlay text
        if result:
            font = pygame.font.SysFont(None, 48)
            surf = font.render(result, True, (255, 0, 0))
            rect = surf.get_rect(center=(width*CELL_SIZE // 2, height*CELL_SIZE // 2))
            screen.blit(surf, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
