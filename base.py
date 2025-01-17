import pygame
import sys
from save import load_data, save_data, reset_save  # Importing from save.py
from game import game_loop  # Importing game_loop from game.py

# Constants
PASTEL_ORANGE = (255, 204, 153)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_YELLOW = (255, 253, 208)
PASTEL_GREEN = (204, 255, 153)

# Load game data
data = load_data()

def settings_menu(screen, font, data):
    screen.fill(PASTEL_YELLOW)

    # Title
    title = font.render("Settings", True, BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

    # Control setting
    controls_text = font.render(f"Controls: {data['controls']}", True, BLACK)
    screen.blit(controls_text, (screen.get_width() // 2 - controls_text.get_width() // 2, 150))

    switch_button = pygame.Rect(screen.get_width() // 2 - 100, 200, 200, 50)
    pygame.draw.rect(screen, (200, 200, 200), switch_button)
    switch_text = font.render("Switch Controls", True, BLACK)
    screen.blit(switch_text, (switch_button.centerx - switch_text.get_width() // 2, switch_button.centery - switch_text.get_height() // 2))

    # Reset save button
    reset_button = pygame.Rect(screen.get_width() // 2 - 100, 300, 200, 50)
    pygame.draw.rect(screen, (200, 50, 50), reset_button)
    reset_text = font.render("Reset Save", True, BLACK)
    screen.blit(reset_text, (reset_button.centerx - reset_text.get_width() // 2, reset_button.centery - reset_text.get_height() // 2))

    # Back to menu button
    back_button = pygame.Rect(screen.get_width() // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, (150, 150, 150), back_button)
    back_text = font.render("Back to Menu", True, BLACK)
    screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))

    pygame.display.flip()

    # Handle events
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(data)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if switch_button.collidepoint(x, y):
                    data["controls"] = "ARROWS" if data["controls"] == "WASD" else "WASD"
                elif reset_button.collidepoint(x, y):
                    reset_save(data)  # Reset save functionality
                elif back_button.collidepoint(x, y):
                    return

            # Redraw menu to update settings
            screen.fill(PASTEL_YELLOW)
            screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
            controls_text = font.render(f"Controls: {data['controls']}", True, BLACK)
            screen.blit(controls_text, (screen.get_width() // 2 - controls_text.get_width() // 2, 150))
            pygame.draw.rect(screen, (200, 200, 200), switch_button)
            screen.blit(switch_text, (switch_button.centerx - switch_text.get_width() // 2, switch_button.centery - switch_text.get_height() // 2))
            pygame.draw.rect(screen, (200, 50, 50), reset_button)
            screen.blit(reset_text, (reset_button.centerx - reset_text.get_width() // 2, reset_button.centery - reset_text.get_height() // 2))
            pygame.draw.rect(screen, (150, 150, 150), back_button)
            screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, back_button.centery - back_text.get_height() // 2))
            pygame.display.flip()


def draw_menu(screen, font, data):
    screen.fill(PASTEL_YELLOW)

    # Title
    title = font.render("Main Menu", True, BLACK)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

    # Total eggs
    eggs_text = font.render(f"Total Eggs: {data['total_eggs']}", True, BLACK)
    screen.blit(eggs_text, (screen.get_width() // 2 - eggs_text.get_width() // 2, 100))

    # Buttons
    start_button_rect = pygame.Rect(screen.get_width() // 2 - 75, 300, 150, 50)
    settings_button_rect = pygame.Rect(screen.get_width() - 60, 10, 50, 50)

    pygame.draw.rect(screen, PASTEL_GREEN, start_button_rect)
    pygame.draw.rect(screen, (200, 200, 200), settings_button_rect)

    # Button text
    start_text = font.render("Start Run", True, BLACK)
    settings_text = font.render("⚙", True, BLACK)

    screen.blit(start_text, (start_button_rect.centerx - start_text.get_width() // 2, start_button_rect.centery - start_text.get_height() // 2))
    screen.blit(settings_text, (settings_button_rect.centerx - settings_text.get_width() // 2, settings_button_rect.centery - settings_text.get_height() // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data(data)  # Save when quitting
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button_rect.collidepoint(x, y):
                    game_loop(data)  # Start the game loop when "Start Run" is clicked
                elif settings_button_rect.collidepoint(x, y):
                    settings_menu(screen, font, data)  # Open settings when the ⚙ button is clicked
