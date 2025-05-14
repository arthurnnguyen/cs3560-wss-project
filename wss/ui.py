import pygame
from wss.map import Map
from wss.player import Player
from wss.brain import Brain, SurvivalBrain, ResourceBrain, RiskyBrain
from wss.vision import CautiousVision, FocusedVision, KeenEyed, FarSight
from wss.item import FoodBonus, WaterBonus, GoldBonus
from wss.trader import Trader
from wss.trade_dialog import show_trade_dialog

# --- SETUP FUNCTION ---
def get_vision_by_name(vision_name):
    """Get Vision by name"""
    vision_map = {
        "cautious": CautiousVision(),
        "focused": FocusedVision(),
        "keen": KeenEyed(),
        "farsight": FarSight()
    }
    return vision_map.get(vision_name.lower(), CautiousVision())

def get_brain_by_name(brain_name):
    """Get Brain by name"""
    brain_map = {
        "survival": SurvivalBrain(),
        "resource": ResourceBrain(),
        "risky": RiskyBrain()
    }
    return brain_map.get(brain_name.lower(), ResourceBrain())

def setup_game():
    global GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT, screen

    # Display screen selecting difficulty level
    pygame.init()
    setup_screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Wilderness Survival Game")
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 28, bold=True)

    # Color
    BLACK = (30, 30, 30)  
    WHITE = (255, 255, 255)
    BUTTON_GREEN = (76, 175, 80)  
    BUTTON_BLUE = (66, 133, 244)  
    BUTTON_DARK = (52, 73, 94)  
    BUTTON_RED = (244, 67, 54)
    BUTTON_YELLOW = (255, 235, 59)
    SELECTED_COLOR = (255, 193, 7)  # Yellow
    INPUT_BG = (45, 45, 45) 

    difficulty = "easy"
    brain_type = "resource"
    vision_type = "cautious"

    grid_width = DEFAULT_GRID_WIDTH
    grid_height = DEFAULT_GRID_HEIGHT

    active_input = None
    width_text = str(grid_width)  # Default values
    height_text = str(grid_height)  # Default values

    width_input_rect = pygame.Rect(250, 400, 100, 32)
    height_input_rect = pygame.Rect(250, 450, 100, 32)

    def draw_selection_screen():
        setup_screen.fill(BLACK)

        title = title_font.render("Wilderness Survival Game", True, WHITE)
        setup_screen.blit(title, (50, 20))

        diff_title = font.render("Select Difficulty Levels:", True, WHITE)
        setup_screen.blit(diff_title, (50, 60))

        diff_buttons = [
            {"text": "Easy", "value": "easy", "rect": pygame.Rect(50, 90, 80, 30), "color": BUTTON_GREEN},
            {"text": "Medium", "value": "medium", "rect": pygame.Rect(150, 90, 100, 30), "color": BUTTON_YELLOW},
            {"text": "Difficult", "value": "hard", "rect": pygame.Rect(260, 90, 80, 30), "color": BUTTON_RED}
        ]

        vision_title = font.render("Select Vision:", True, WHITE)
        setup_screen.blit(vision_title, (50, 140))

        vision_buttons = [
            {"text": "Focused", "value": "focused", "rect": pygame.Rect(50, 170, 100, 30), "color": BUTTON_BLUE},
            {"text": "Cautious", "value": "cautious", "rect": pygame.Rect(160, 170, 100, 30), "color": BUTTON_BLUE},
            {"text": "KeenEyed", "value": "keen", "rect": pygame.Rect(270, 170, 80, 30), "color": BUTTON_BLUE},
            {"text": "Far Sight", "value": "farsight", "rect": pygame.Rect(150, 210, 100, 30), "color": BUTTON_BLUE}
        ]

        brain_title = font.render("Select Brain:", True, WHITE)
        setup_screen.blit(brain_title, (50, 260))

        brain_buttons = [
            {"text": "Survival", "value": "survival", "rect": pygame.Rect(50, 290, 100, 30), "color": BUTTON_BLUE},
            {"text": "Resource", "value": "resource", "rect": pygame.Rect(160, 290, 100, 30), "color": BUTTON_GREEN},
            {"text": "Risky", "value": "risky", "rect": pygame.Rect(270, 290, 80, 30), "color": BUTTON_BLUE}
        ]

        map_size_title = font.render("Size of the map:", True, WHITE)
        setup_screen.blit(map_size_title, (50, 350))

        width_label = font.render(f"Width (2-{MAX_GRID_WIDTH}):", True, WHITE)
        setup_screen.blit(width_label, (50, 400))

        if active_input == "width":
            color = SELECTED_COLOR
        else:
            color = INPUT_BG
        pygame.draw.rect(setup_screen, color, width_input_rect, border_radius=3)
        width_surface = font.render(width_text, True, WHITE)
        setup_screen.blit(width_surface, (width_input_rect.x + 5, width_input_rect.y + 5))

        height_label = font.render(f"Height (2-{MAX_GRID_HEIGHT}):", True, WHITE)
        setup_screen.blit(height_label, (50, 450))

        if active_input == "height":
            color = SELECTED_COLOR
        else:
            color = INPUT_BG
        pygame.draw.rect(setup_screen, color, height_input_rect, border_radius=3)
        height_surface = font.render(height_text, True, WHITE)
        setup_screen.blit(height_surface, (height_input_rect.x + 5, height_input_rect.y + 5))

        start_button = pygame.Rect(200, 500, 100, 40)

        for btn in diff_buttons:
            color = SELECTED_COLOR if btn["value"] == difficulty else btn["color"]
            pygame.draw.rect(setup_screen, color, btn["rect"], border_radius=5)
            text = font.render(btn["text"], True, WHITE)
            text_rect = text.get_rect(center=btn["rect"].center)
            setup_screen.blit(text, text_rect)

        for btn in vision_buttons:
            color = SELECTED_COLOR if btn["value"] == vision_type else btn["color"]
            pygame.draw.rect(setup_screen, color, btn["rect"], border_radius=5)
            text = font.render(btn["text"], True, WHITE)
            text_rect = text.get_rect(center=btn["rect"].center)
            setup_screen.blit(text, text_rect)

        for btn in brain_buttons:
            color = SELECTED_COLOR if btn["value"] == brain_type else btn["color"]
            pygame.draw.rect(setup_screen, color, btn["rect"], border_radius=5)
            text = font.render(btn["text"], True, WHITE)
            text_rect = text.get_rect(center=btn["rect"].center)
            setup_screen.blit(text, text_rect)

        pygame.draw.rect(setup_screen, BUTTON_GREEN, start_button, border_radius=5)
        start_text = font.render("Start", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button.center)
        setup_screen.blit(start_text, start_text_rect)

        pygame.display.flip()
        return start_button, diff_buttons, vision_buttons, brain_buttons, width_input_rect, height_input_rect

    selecting = True
    while selecting:
        start_button, diff_buttons, vision_buttons, brain_buttons, width_input_rect, height_input_rect = draw_selection_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None

            if event.type == pygame.KEYDOWN:
             
                if active_input == "width":
                    if event.key == pygame.K_BACKSPACE:
                        width_text = width_text[:-1]
                        if width_text == "":
                            width_text = ""
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        active_input = "height"
                    elif event.unicode.isdigit():
                        if len(width_text) < 3:
                            width_text += event.unicode
                elif active_input == "height":
                    if event.key == pygame.K_BACKSPACE:
                        height_text = height_text[:-1]
                        if height_text == "":
                            height_text = ""
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        active_input = None
                    elif event.unicode.isdigit():
                        if len(height_text) < 3:
                            height_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()

                if start_button.collidepoint(pos):
                    try:
                        if width_text == "":
                            width_text = str(DEFAULT_GRID_WIDTH)
                        if height_text == "":
                            height_text = str(DEFAULT_GRID_HEIGHT)

                        width_value = int(width_text)
                        height_value = int(height_text)
                        grid_width = max(2, min(width_value, MAX_GRID_WIDTH))
                        grid_height = max(2, min(height_value, MAX_GRID_HEIGHT))
                        print(f"Size of Map: {grid_width}x{grid_height}")

                        selecting = False
                    except ValueError:
                        grid_width = DEFAULT_GRID_WIDTH
                        grid_height = DEFAULT_GRID_HEIGHT
                        print(f"Use default size: {grid_width}x{grid_height}")
                        selecting = False

                for btn in diff_buttons:
                    if btn["rect"].collidepoint(pos):
                        difficulty = btn["value"]

                for btn in vision_buttons:
                    if btn["rect"].collidepoint(pos):
                        vision_type = btn["value"]

                for btn in brain_buttons:
                    if btn["rect"].collidepoint(pos):
                        brain_type = btn["value"]

                if width_input_rect.collidepoint(pos):
                    active_input = "width"
                elif height_input_rect.collidepoint(pos):
                    active_input = "height"
                else:
                    active_input = None

    GRID_WIDTH = grid_width
    GRID_HEIGHT = grid_height
    WIDTH = TILE_SIZE * GRID_WIDTH
    HEIGHT = TILE_SIZE * GRID_HEIGHT + INFO_HEIGHT + CONTROL_HEIGHT

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wilderness Survival Game")
    game_map = Map(width=GRID_WIDTH, height=GRID_HEIGHT, difficulty=difficulty)
    brain = None if brain_type == "none" else get_brain_by_name(brain_type)
    vision = get_vision_by_name(vision_type)
    location = (0, 0)
    player = Player(
        max_strength=30,
        max_water=30,
        max_food=30,
        vision=vision,
        brain=brain,
        location=location
    )
    game_map.get_square(2, 2).add_item(FoodBonus(amount=3))
    game_map.get_square(5, 3).add_item(FoodBonus(amount=5))

    game_map.get_square(3, 1).add_item(WaterBonus(amount=3))
    game_map.get_square(7, 2).add_item(WaterBonus(amount=5))

    game_map.get_square(4, 4).add_item(GoldBonus(amount=2))
    game_map.get_square(8, 1).add_item(GoldBonus(amount=3))

    game_map.get_square(6, 6).add_item(Trader())

    game_map.get_square(1, 1).add_item(Trader())

    return game_map, player

# --- INIT ---
pygame.init()
TILE_SIZE = 35  
MAX_SCREEN_WIDTH = 1200
MAX_SCREEN_HEIGHT = 800
MAX_GRID_WIDTH = MAX_SCREEN_WIDTH // TILE_SIZE
MAX_GRID_HEIGHT = (MAX_SCREEN_HEIGHT - 100) // TILE_SIZE  
DEFAULT_GRID_WIDTH = 12
DEFAULT_GRID_HEIGHT = 12
INFO_HEIGHT = 30  
CONTROL_HEIGHT = 50  
GRID_WIDTH = DEFAULT_GRID_WIDTH
GRID_HEIGHT = DEFAULT_GRID_HEIGHT
WIDTH = TILE_SIZE * GRID_WIDTH
HEIGHT = TILE_SIZE * GRID_HEIGHT + INFO_HEIGHT + CONTROL_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Wilderness Survival Game")
font = pygame.font.SysFont(None, 20)  
title_font = pygame.font.SysFont(None, 24, bold=True)

COLORS = {
    "background": (30, 30, 30),  
    "plain": (76, 175, 80),  
    "forest": (27, 94, 32),  
    "mountain": (121, 85, 72),  
    "water": (33, 150, 243),  
    "player": (244, 67, 54),  
    "player_highlight": (255, 235, 59),  
    "player_border": (255, 152, 0),  
    "food": (255, 193, 7),  
    "water_item": (3, 169, 244),  
    "gold": (255, 215, 0),  
    "trader": (233, 30, 99), 
    "button": (66, 133, 244),  
    "button_green": (76, 175, 80),  
    "button_blue": (66, 133, 244),  
    "button_dark": (52, 73, 94), 
    "text": (255, 255, 255),  
    "title": (255, 255, 255)  
}

game_map, player = setup_game()

steps_count = 0
high_score = 0 

traded_squares = set()

# --- DRAWING FUNCTIONS ---
def draw_grid(show_resources=False):
    visible_squares = []
    if player.vision:
        visible_squares = player.vision.get_visible_squares(game_map, player)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = game_map.grid[y][x]
            terrain = square.terrain.name.lower()
            color = COLORS.get(terrain, COLORS["background"])

            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            pygame.draw.rect(screen, (50, 50, 50),
                           (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

            if (x, y) in visible_squares:
                pygame.draw.rect(screen, COLORS["player_highlight"],
                               (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)  

                if square.items:
                    for item in square.items:
                        if isinstance(item, FoodBonus):
                            pygame.draw.circle(screen, COLORS["food"],
                                              (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                              TILE_SIZE // 4)
                        elif isinstance(item, WaterBonus):

                            pygame.draw.circle(screen, COLORS["water_item"],
                                              (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                              TILE_SIZE // 4)
                        elif isinstance(item, GoldBonus):

                            pygame.draw.circle(screen, COLORS["gold"],
                                              (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                              TILE_SIZE // 4)
                        elif isinstance(item, Trader):
                            pygame.draw.circle(screen, COLORS["trader"],
                                              (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2),
                                              TILE_SIZE // 3)

            elif show_resources and square.items:
                for item in square.items:
                    if isinstance(item, FoodBonus):
                        s = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*COLORS["food"], 128),  
                                          (TILE_SIZE//4, TILE_SIZE//4),
                                          TILE_SIZE // 4)
                        screen.blit(s, (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4))
                    elif isinstance(item, WaterBonus):
                        s = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*COLORS["water_item"], 128),
                                          (TILE_SIZE//4, TILE_SIZE//4),
                                          TILE_SIZE // 4)
                        screen.blit(s, (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4))
                    elif isinstance(item, GoldBonus):
                        s = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*COLORS["gold"], 128),
                                          (TILE_SIZE//4, TILE_SIZE//4),
                                          TILE_SIZE // 4)
                        screen.blit(s, (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4))
                    elif isinstance(item, Trader):
                        s = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*COLORS["trader"], 128),
                                          (TILE_SIZE//4, TILE_SIZE//4),
                                          TILE_SIZE // 3)
                        screen.blit(s, (x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4))

def draw_player():
    x, y = player.location

    for i in range(5, 0, -1):
        alpha = 50 - i * 10  
        s = pygame.Surface((TILE_SIZE + i*4, TILE_SIZE + i*4), pygame.SRCALPHA)
        s.fill((255, 255, 0, alpha))
        screen.blit(s, (x * TILE_SIZE - i*2, y * TILE_SIZE - i*2))

    pygame.draw.rect(screen, COLORS["player_highlight"],
                    (x * TILE_SIZE - 4, y * TILE_SIZE - 4, TILE_SIZE + 8, TILE_SIZE + 8))

    pygame.draw.rect(screen, COLORS["player_border"],
                    (x * TILE_SIZE - 2, y * TILE_SIZE - 2, TILE_SIZE + 4, TILE_SIZE + 4))

    pygame.draw.rect(screen, COLORS["player"],
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_stats():
    stats_surface = pygame.Surface((WIDTH, INFO_HEIGHT))
    stats_surface.fill((0, 0, 0)) 
    stats_text = f"Strength: {player.current_strength} | Water: {player.current_water} | Food: {player.current_food} | Gold: {player.current_gold} | Step: {steps_count}"
    stats_render = font.render(stats_text, True, COLORS["text"])
    stats_surface.blit(stats_render, (10, 8))

    if high_score > 0:
        high_score_text = f"Record: {high_score} step"
        high_score_render = font.render(high_score_text, True, COLORS["text"])
        stats_surface.blit(high_score_render, (WIDTH - 150, 8))

    screen.blit(stats_surface, (0, GRID_HEIGHT * TILE_SIZE))

def draw_buttons():
    button_surface = pygame.Surface((WIDTH, CONTROL_HEIGHT))
    button_surface.fill((0, 0, 0))  

    button_width = 60
    button_height = 30
    spacing = 3

    total_buttons_width = 6 * button_width + 5 * spacing  
    start_x = (WIDTH - total_buttons_width) // 2

    rest_rect = pygame.Rect(start_x, 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_green"], rest_rect, border_radius=3)
    rest_text = font.render("Rest", True, COLORS["text"])
    rest_text_rect = rest_text.get_rect(center=rest_rect.center)
    button_surface.blit(rest_text, rest_text_rect)

    bac_rect = pygame.Rect(start_x + button_width + spacing, 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_blue"], bac_rect, border_radius=3)
    bac_text = font.render("North", True, COLORS["text"])
    bac_text_rect = bac_text.get_rect(center=bac_rect.center)
    button_surface.blit(bac_text, bac_text_rect)

    nam_rect = pygame.Rect(start_x + 2 * (button_width + spacing), 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_blue"], nam_rect, border_radius=3)
    nam_text = font.render("South", True, COLORS["text"])
    nam_text_rect = nam_text.get_rect(center=nam_rect.center)
    button_surface.blit(nam_text, nam_text_rect)

    tay_rect = pygame.Rect(start_x + 3 * (button_width + spacing), 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_blue"], tay_rect, border_radius=3)
    tay_text = font.render("West", True, COLORS["text"])
    tay_text_rect = tay_text.get_rect(center=tay_rect.center)
    button_surface.blit(tay_text, tay_text_rect)

    dong_rect = pygame.Rect(start_x + 4 * (button_width + spacing), 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_blue"], dong_rect, border_radius=3)
    dong_text = font.render("East", True, COLORS["text"])
    dong_text_rect = dong_text.get_rect(center=dong_rect.center)
    button_surface.blit(dong_text, dong_text_rect)

    hint_rect = pygame.Rect(start_x + 5 * (button_width + spacing), 10, button_width, button_height)
    pygame.draw.rect(button_surface, COLORS["button_dark"], hint_rect, border_radius=3)
    hint_text = font.render("Hint", True, COLORS["text"])
    hint_text_rect = hint_text.get_rect(center=hint_rect.center)
    button_surface.blit(hint_text, hint_text_rect)

    screen.blit(button_surface, (0, GRID_HEIGHT * TILE_SIZE + INFO_HEIGHT))

def get_clicked_direction(pos):
    x, y = pos

    if y < GRID_HEIGHT * TILE_SIZE or y > GRID_HEIGHT * TILE_SIZE + INFO_HEIGHT + CONTROL_HEIGHT:
        return None

    button_y = y - (GRID_HEIGHT * TILE_SIZE + INFO_HEIGHT)

    button_width = 60
    button_height = 30
    spacing = 3

    total_buttons_width = 6 * button_width + 5 * spacing
    start_x = (WIDTH - total_buttons_width) // 2

    rest_rect = pygame.Rect(start_x, 10, button_width, button_height)
    if rest_rect.collidepoint(x, button_y):
        return "rest"

    bac_rect = pygame.Rect(start_x + button_width + spacing, 10, button_width, button_height)
    if bac_rect.collidepoint(x, button_y):
        return (0, -1)  

    nam_rect = pygame.Rect(start_x + 2 * (button_width + spacing), 10, button_width, button_height)
    if nam_rect.collidepoint(x, button_y):
        return (0, 1)  

    tay_rect = pygame.Rect(start_x + 3 * (button_width + spacing), 10, button_width, button_height)
    if tay_rect.collidepoint(x, button_y):
        return (-1, 0)  

    dong_rect = pygame.Rect(start_x + 4 * (button_width + spacing), 10, button_width, button_height)
    if dong_rect.collidepoint(x, button_y):
        return (1, 0)  

    hint_rect = pygame.Rect(start_x + 5 * (button_width + spacing), 10, button_width, button_height)
    if hint_rect.collidepoint(x, button_y):
        return "hint"

    return None

# --- HINT FUNCTION ---
def display_hint():
    """ Display hints for users """
    if not player.vision:
        return False

    current_screen = screen.copy()

    screen.fill(COLORS["background"])
    draw_grid(show_resources=True)
    draw_player()

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  
    screen.blit(overlay, (0, 0))

    hint_box_width = WIDTH - 40
    hint_box_height = 200
    hint_surface = pygame.Surface((hint_box_width, hint_box_height))
    hint_surface.fill((30, 30, 30))  

    pygame.draw.rect(hint_surface, COLORS["button_blue"], (0, 0, hint_box_width, hint_box_height), 2)

    y_pos = 10

    title_text = title_font.render("--- Hints ---", True, COLORS["text"])
    hint_surface.blit(title_text, (hint_box_width // 2 - title_text.get_width() // 2, y_pos))
    y_pos += 30

    if player.brain:
        brain_type = type(player.brain).__name__
        brain_map = {
            "SurvivalBrain": "Survival",
            "ResourceBrain": "Resource",
            "RiskyBrain": "Risky"
        }
        brain_name = brain_map.get(brain_type, brain_type)

        text = font.render(f"[Suggestion from {brain_name}]", True, COLORS["text"])
        hint_surface.blit(text, (20, y_pos))
        y_pos += 25

        suggestion = player.brain.suggest_move(game_map, player)
        if suggestion:
            direction_names = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West', 'r': 'Rest'}
            for direction, reason in suggestion.items():
                if direction in direction_names:
                    if "Resources" in reason:
                        reason = "Resource in this direction"
                    elif "Direction" in reason:
                        reason = "Best path"
                    elif "Near" in reason:
                        reason = "Near resource"
                    elif "Recover" in reason:
                        reason = "Recover strength"
                    else:
                        reason = "Good choice!"

                    if direction == 'r':
                        text = font.render(f"- Should {direction_names[direction]}: {reason}", True, COLORS["text"])
                    else:
                        text = font.render(f"- Should move in this direction {direction_names[direction]}: {reason}", True, COLORS["text"])
                    hint_surface.blit(text, (20, y_pos))
                    y_pos += 25
        else:
            text = font.render("- No suggestions available.", True, COLORS["text"])
            hint_surface.blit(text, (20, y_pos))
            y_pos += 25
    else:
        text = font.render("No brain to give suggestions.", True, COLORS["text"])
        hint_surface.blit(text, (20, y_pos))
        y_pos += 25

    exit_text = font.render("Press a random button to resume the game", True, COLORS["text"])
    hint_surface.blit(exit_text, (hint_box_width // 2 - exit_text.get_width() // 2, hint_box_height - 30))

    screen.blit(hint_surface, (20, (HEIGHT - hint_box_height) // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                return True  
    screen.blit(current_screen, (0, 0))
    pygame.display.flip()

    return False  

# --- MAIN LOOP ---
running = True
clock = pygame.time.Clock()
show_path_info = False 
show_hint = False  

def display_path_info():
    if not player.vision:
        return False

    current_screen = screen.copy()

    screen.fill(COLORS["background"])
    draw_grid()
    draw_player()

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  
    screen.blit(overlay, (0, 0))
    info_box_width = WIDTH - 40
    info_box_height = 300
    info_surface = pygame.Surface((info_box_width, info_box_height))
    info_surface.fill((30, 30, 30)) 
    pygame.draw.rect(info_surface, COLORS["button_green"], (0, 0, info_box_width, info_box_height), 2)

    y_pos = 10
    vision_type = type(player.vision).__name__
    vision_map = {
        "FocusedVision": "Focused",
        "CautiousVision": "Cautious",
        "KeenEyed": "KeenEyed",
        "FarSight": "FarSight"
    }
    vision_name = vision_map.get(vision_type, vision_type)

    title_text = title_font.render(f"Path Information (Vision: {vision_name})", True, COLORS["text"])
    info_surface.blit(title_text, (info_box_width // 2 - title_text.get_width() // 2, y_pos))
    y_pos += 30

    food_path = player.vision.closest_food(game_map, player)
    if food_path:
        text = font.render(f"Nearest food: {food_path.end_position}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        directions_text = " -> ".join([d.replace("Move-", "") for d in food_path.directions])
        text = font.render(f"Direction: {directions_text}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        cost = food_path.total_cost()
        text = font.render(f"Cost: Strength={cost['movement']}, Food={cost['food']}, Water={cost['water']}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30

    else:
        text = font.render("No food in sight.", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30

    water_path = player.vision.closest_water(game_map, player)
    if water_path:
        text = font.render(f"Nearest water: {water_path.end_position}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        directions_text = " -> ".join([d.replace("Move-", "") for d in water_path.directions])
        text = font.render(f"Direction: {directions_text}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        cost = water_path.total_cost()
        text = font.render(f"Cost: Strength={cost['movement']}, Food={cost['food']}, Water={cost['water']}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30
    else:
        text = font.render("No water in sight.", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30

    if vision_type in ["KeenEyed", "FarSight"]:
        gold_path = player.vision.closest_gold(game_map, player)
        if gold_path:
            text = font.render(f"Nearest gold: {gold_path.end_position}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 20

            directions_text = " -> ".join([d.replace("Move-", "") for d in gold_path.directions])
            text = font.render(f"Direction: {directions_text}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 20

            cost = gold_path.total_cost()
            text = font.render(f"Cost: Strength={cost['movement']}, Food={cost['food']}, Water={cost['water']}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 30
        else:
            text = font.render("No gold in sight.", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 30

    if vision_type == "FarSight":
        trader_path = player.vision.closest_trader(game_map, player)
        if trader_path:
            text = font.render(f"Nearest trader: {trader_path.end_position}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 20

            directions_text = " -> ".join([d.replace("Move-", "") for d in trader_path.directions])
            text = font.render(f"Direction: {directions_text}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 20

            cost = trader_path.total_cost()
            text = font.render(f"Cost: Strength={cost['movement']}, Food={cost['food']}, Water={cost['water']}", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 30
        else:
            text = font.render("No trader in sight.", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 30

    easy_path = player.vision.easiest_path(game_map, player)
    if easy_path:
        text = font.render(f"Easiest path: {easy_path.end_position}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        directions_text = " -> ".join([d.replace("Move-", "") for d in easy_path.directions])
        text = font.render(f"Direction: {directions_text}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        cost = easy_path.total_cost()
        text = font.render(f"Cost: Strength={cost['movement']}, Food={cost['food']}, Water={cost['water']}", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30
    else:
        text = font.render("Cannot find the easiest path.", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 30

    if player.brain:
        brain_type = type(player.brain).__name__
        brain_map = {
            "SurvivalBrain": "Survival",
            "ResourceBrain": "Resource",
            "RiskyBrain": "Risky"
        }
        brain_name = brain_map.get(brain_type, brain_type)

        text = font.render(f"[Hint from {brain_name}]", True, COLORS["text"])
        info_surface.blit(text, (20, y_pos))
        y_pos += 20

        suggestion = player.brain.suggest_move(game_map, player)
        if suggestion:
            direction_names = {'n': 'North', 's': 'South', 'e': 'East', 'w': 'West', 'r': 'Rest'}
            for direction, reason in suggestion.items():
                if direction in direction_names:
                    if "Resource" in reason:
                        reason = "Resource in this direction"
                    elif "step" in reason:
                        reason = "Best move"
                    elif "near" in reason:
                        reason = "Close to resource"
                    elif "recover" in reason:
                        reason = "Recover strength"
                    else:
                        reason = "Good choice!"

                    if direction == 'r':
                        text = font.render(f"- Should {direction_names[direction]}: {reason}", True, COLORS["text"])
                    else:
                        text = font.render(f"- Should move in the direction {direction_names[direction]}: {reason}", True, COLORS["text"])
                    info_surface.blit(text, (20, y_pos))
                    y_pos += 20
        else:
            text = font.render("- No suggestion available.", True, COLORS["text"])
            info_surface.blit(text, (20, y_pos))
            y_pos += 20

    exit_text = font.render("Press any button to resume the game", True, COLORS["text"])
    info_surface.blit(exit_text, (info_box_width // 2 - exit_text.get_width() // 2, info_box_height - 30))

    screen.blit(info_surface, (20, (HEIGHT - info_box_height) // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            if event.type == pygame.QUIT:
                return True  

    screen.blit(current_screen, (0, 0))
    pygame.display.flip()

    return False  

while running:
    screen.fill(COLORS["background"])
    draw_grid()  
    draw_player()
    draw_stats()
    draw_buttons()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if player.move((0, -1), game_map):  
                    steps_count += 1
            elif event.key == pygame.K_DOWN:
                if player.move((0, 1), game_map):  
                    steps_count += 1
            elif event.key == pygame.K_LEFT:
                if player.move((-1, 0), game_map):  
                    steps_count += 1
            elif event.key == pygame.K_RIGHT:
                if player.move((1, 0), game_map):  
                    steps_count += 1
            elif event.key == pygame.K_r:
                player.rest()  
            elif event.key == pygame.K_i:
                show_path_info = True  
            elif event.key == pygame.K_h:
                show_hint = True  

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            action = get_clicked_direction(event.pos)
            if action:
                if action == "rest":
                    player.rest()
                    print("You have rested (+2 Strength, -0.5 Food & Water).")
                elif action == "info":
                    show_path_info = True
                elif action == "hint":
                    show_hint = True
                else:
                    if player.move(action, game_map):
                        steps_count += 1

    if show_path_info:
        quit_game = display_path_info()
        if quit_game:
            running = False
        show_path_info = False

    if show_hint:
        quit_game = display_hint()
        if quit_game:
            running = False
        show_hint = False

    current_pos = player.location
    current_square = game_map.get_square(current_pos[0], current_pos[1])
    if current_square and current_square.has_trader() and current_pos not in traded_squares:
        for item in current_square.items[:]:
            if isinstance(item, Trader):
                trade_accepted = show_trade_dialog(screen, player, item)
                traded_squares.add(current_pos)
                screen.fill(COLORS["background"])
                draw_grid()
                draw_player()
                draw_stats()
                draw_buttons()
                pygame.display.flip()
                break

    if player.location[0] >= GRID_WIDTH - 1:
        if high_score == 0 or steps_count < high_score:
            high_score = steps_count
            new_record = True
        else:
            new_record = False

        win_surface = pygame.Surface((WIDTH, HEIGHT))
        win_surface.fill((0, 0, 0))
        win_text = font.render("Congratulations! You have reached the East coast and survived!", True, (0, 255, 0))
        win_surface.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))

        steps_text = font.render(f"Number of steps: {steps_count}", True, COLORS["text"])
        win_surface.blit(steps_text, (WIDTH // 2 - steps_text.get_width() // 2, HEIGHT // 2 - 30))

        if new_record:
            record_text = font.render(f"NEW RECORD: {high_score} steps!", True, (255, 215, 0))  # Màu vàng
        else:
            record_text = font.render(f"Record: {high_score} steps", True, COLORS["text"])
        win_surface.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, HEIGHT // 2))

        
        replay_button_width = 120
        replay_button_height = 40
        replay_button = pygame.Rect(WIDTH // 2 - replay_button_width - 10, HEIGHT // 2 + 40, replay_button_width, replay_button_height)
        pygame.draw.rect(win_surface, COLORS["button_green"], replay_button, border_radius=5)
        replay_text = font.render("Replay", True, COLORS["text"])
        replay_text_rect = replay_text.get_rect(center=replay_button.center)
        win_surface.blit(replay_text, replay_text_rect)

    
        exit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 40, replay_button_width, replay_button_height)
        pygame.draw.rect(win_surface, COLORS["button_dark"], exit_button, border_radius=5)
        exit_text = font.render("Quit", True, COLORS["text"])
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        win_surface.blit(exit_text, exit_text_rect)

        screen.blit(win_surface, (0, 0))
        pygame.display.flip()
        waiting = True
        restart_game = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_button.collidepoint(mouse_pos):
                        restart_game = True
                        waiting = False
                    elif exit_button.collidepoint(mouse_pos):
                        waiting = False
                if event.type == pygame.QUIT:
                    waiting = False

        if restart_game:
            game_map, player = setup_game()
            steps_count = 0
            traded_squares.clear()
        else:
            running = False

    if player.current_strength <= 0 or player.current_food <= 0 or player.current_water <= 0:
        lose_surface = pygame.Surface((WIDTH, HEIGHT))
        lose_surface.fill((0, 0, 0))

        reason = ""
        if player.current_strength <= 0:
            reason = "tired"
        elif player.current_food <= 0:
            reason = "hungry"
        elif player.current_water <= 0:
            reason = "thristy"

        lose_text = font.render(f"You are {reason} and cannot survive. Game over.", True, (255, 0, 0))
        lose_surface.blit(lose_text, (WIDTH // 2 - lose_text.get_width() // 2, HEIGHT // 2 - 60))

        stats_text = font.render(f"Strength: {player.current_strength}, Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}", True, COLORS["text"])
        lose_surface.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2 - 30))

        # Display steps taken
        steps_text = font.render(f"Number of steps: {steps_count}", True, COLORS["text"])
        lose_surface.blit(steps_text, (WIDTH // 2 - steps_text.get_width() // 2, HEIGHT // 2))

        # Display highest scores
        if high_score > 0:
            record_text = font.render(f"Record: {high_score} steps", True, COLORS["text"])
            lose_surface.blit(record_text, (WIDTH // 2 - record_text.get_width() // 2, HEIGHT // 2 + 30))

        # Replay button
        replay_button_width = 120
        replay_button_height = 40
        replay_button = pygame.Rect(WIDTH // 2 - replay_button_width - 10, HEIGHT // 2 + 20, replay_button_width, replay_button_height)
        pygame.draw.rect(lose_surface, COLORS["button_green"], replay_button, border_radius=5)
        replay_text = font.render("Replay", True, COLORS["text"])
        replay_text_rect = replay_text.get_rect(center=replay_button.center)
        lose_surface.blit(replay_text, replay_text_rect)

        # Exit button
        exit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 20, replay_button_width, replay_button_height)
        pygame.draw.rect(lose_surface, COLORS["button_dark"], exit_button, border_radius=5)
        exit_text = font.render("Quit", True, COLORS["text"])
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        lose_surface.blit(exit_text, exit_text_rect)

        screen.blit(lose_surface, (0, 0))
        pygame.display.flip()

        # Waiting for the user to click the buttons
        waiting = True
        restart_game = False
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay_button.collidepoint(mouse_pos):
                        restart_game = True
                        waiting = False
                    elif exit_button.collidepoint(mouse_pos):
                        waiting = False
                if event.type == pygame.QUIT:
                    waiting = False

        if restart_game:
            # Restart the game
            game_map, player = setup_game()
            # Count steps
            steps_count = 0
            
            traded_squares.clear()
        else:
            running = False

    clock.tick(10)

pygame.quit()
