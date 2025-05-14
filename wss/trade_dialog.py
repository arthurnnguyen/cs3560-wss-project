import pygame

def show_trade_dialog(screen, player, trader):
    current_screen = screen.copy()
    screen_width, screen_height = screen.get_size()
    
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  
    screen.blit(overlay, (0, 0))
    
    dialog_width = 400
    dialog_height = 250
    dialog_surface = pygame.Surface((dialog_width, dialog_height))
    dialog_surface.fill((30, 30, 30))  
    
    pygame.draw.rect(dialog_surface, (66, 133, 244), (0, 0, dialog_width, dialog_height), 2)
    
    title_font = pygame.font.SysFont(None, 28, bold=True)
    font = pygame.font.SysFont(None, 24)
    
    title_text = title_font.render("Trading offer", True, (255, 255, 255))
    dialog_surface.blit(title_text, (dialog_width // 2 - title_text.get_width() // 2, 20))
    
    offer_text = font.render("Trader: I have an offer for you.", True, (255, 255, 255))
    dialog_surface.blit(offer_text, (20, 60))
    
    trade_text = font.render("Give me 2 Food and 1 Water, I will give you 3 Gold.", True, (255, 255, 255))
    dialog_surface.blit(trade_text, (20, 90))
    
    resource_text = font.render(f"Current resource: Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}", True, (255, 255, 255))
    dialog_surface.blit(resource_text, (20, 120))
    
    has_resources = player.current_food >= 2 and player.current_water >= 1
    
    if not has_resources:
        warning_text = font.render("You don't have enough resource for this trade!", True, (255, 0, 0))
        dialog_surface.blit(warning_text, (20, 150))
    
    accept_button_width = 120
    accept_button_height = 40
    accept_button = pygame.Rect(dialog_width // 2 - accept_button_width - 10, 180, accept_button_width, accept_button_height)
    
    accept_color = (76, 175, 80) if has_resources else (100, 100, 100)
    pygame.draw.rect(dialog_surface, accept_color, accept_button, border_radius=5)
    accept_text = font.render("Accept", True, (255, 255, 255))
    accept_text_rect = accept_text.get_rect(center=accept_button.center)
    dialog_surface.blit(accept_text, accept_text_rect)
    
    decline_button = pygame.Rect(dialog_width // 2 + 10, 180, accept_button_width, accept_button_height)
    pygame.draw.rect(dialog_surface, (52, 73, 94), decline_button, border_radius=5)
    decline_text = font.render("Reject", True, (255, 255, 255))
    decline_text_rect = decline_text.get_rect(center=decline_button.center)
    dialog_surface.blit(decline_text, decline_text_rect)
    
    dialog_x = (screen_width - dialog_width) // 2
    dialog_y = (screen_height - dialog_height) // 2
    screen.blit(dialog_surface, (dialog_x, dialog_y))
    pygame.display.flip()
    
    waiting = True
    accepted = False
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                dialog_mouse_pos = (mouse_pos[0] - dialog_x, mouse_pos[1] - dialog_y)
                
                if accept_button.collidepoint(dialog_mouse_pos) and has_resources:
                    accepted = True
                    waiting = False
                elif decline_button.collidepoint(dialog_mouse_pos):
                    waiting = False
            if event.type == pygame.QUIT:
                return False
    
    if accepted:
        player.current_food -= 2
        player.current_water -= 1
        player.current_gold += 3
        
        result_surface = pygame.Surface((dialog_width, dialog_height))
        result_surface.fill((30, 30, 30))
        pygame.draw.rect(result_surface, (76, 175, 80), (0, 0, dialog_width, dialog_height), 2)
        
        success_title = title_font.render("Trade successful!", True, (255, 255, 255))
        result_surface.blit(success_title, (dialog_width // 2 - success_title.get_width() // 2, 20))
        
        result_text = font.render("You've exchanged 2 Food and 1 Water to get 3 Gold.", True, (255, 255, 255))
        result_surface.blit(result_text, (20, 60))
        
        new_resource_text = font.render(f"Current resource: Food: {player.current_food}, Water: {player.current_water}, Gold: {player.current_gold}", True, (255, 255, 255))
        result_surface.blit(new_resource_text, (20, 90))
        
        continue_button = pygame.Rect(dialog_width // 2 - accept_button_width // 2, 150, accept_button_width, accept_button_height)
        pygame.draw.rect(result_surface, (66, 133, 244), continue_button, border_radius=5)
        continue_text = font.render("Continue", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_button.center)
        result_surface.blit(continue_text, continue_text_rect)
        
        screen.blit(result_surface, (dialog_x, dialog_y))
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    dialog_mouse_pos = (mouse_pos[0] - dialog_x, mouse_pos[1] - dialog_y)
                    if continue_button.collidepoint(dialog_mouse_pos):
                        waiting = False
                if event.type == pygame.QUIT:
                    return False
    
    screen.blit(current_screen, (0, 0))
    pygame.display.flip()
    
    return accepted
