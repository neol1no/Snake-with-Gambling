import pygame
import os
import subprocess
from game import game_loop
from save import load_save, save_data, reset_save

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
PLAY_AREA = pygame.Rect(100, 100, 600, 400)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Dungeon")

# Colors
PASTEL_YELLOW = (255, 253, 208)
PASTEL_ORANGE = (255, 200, 124)
GREEN = (144, 238, 144)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Load save data
save_data_content = load_save()
current_controls = {"scheme": "WASD"}  # Default control scheme


# Restart the application
def restart_application():
    save_data(save_data_content)  # Save current progress
    pygame.quit()
    subprocess.run(["python", "base.py"])


# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()


# Main menu
def main_menu():
    running = True

    def start_game():
        game_loop(save_data_content, current_controls, PLAY_AREA)
        restart_application()

    def open_store():
        import store
        store.store_loop(save_data_content)
        restart_application()

    def open_gambling():
        import gambling
        gambling.gambling_menu(save_data_content)
        restart_application()

    buttons = [
        Button(300, 150, 200, 50, "Start Game", GREEN, start_game),
        Button(300, 250, 200, 50, "Store", ORANGE, open_store),
        Button(300, 350, 200, 50, "Gambling", ORANGE, open_gambling),
        Button(300, 450, 200, 50, "Exit", RED, exit)
    ]

    while running:
        screen.fill(PASTEL_YELLOW)
        # Draw title
        title_surf = font.render("Snake Dungeon", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surf, title_rect)

        # Draw total eggs
        total_eggs_text = f"Total Eggs: {save_data_content['total_eggs']}"
        total_eggs_surf = font.render(total_eggs_text, True, BLACK)
        screen.blit(total_eggs_surf, (10, 10))

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(event.pos)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_menu()

