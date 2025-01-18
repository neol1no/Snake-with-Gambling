# Import necessary modules
import pygame
import json
import os
from game import game_loop
from save import reset_save, load_save, save_data

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Dungeon")

# Colors
PASTEL_YELLOW = (255, 253, 208)
GREEN = (144, 238, 144)
PASTEL_ORANGE = (255, 200, 124)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Button Class
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

# Save Data and Controls Initialization
save_data_content = load_save()
current_controls = {"scheme": "WASD"}  # Default control scheme

# Function Definitions
def start_run():
    print("Starting the game...")  # Debugging
    pygame.init()  # Restart the pygame display surface
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Dungeon")
    game_loop(save_data_content, current_controls)

def open_store():
    print("Opening store...")  # Debugging
    # store_loop(save_data_content)

def open_gambling():
    print("Opening gambling...")  # Debugging
    # gambling_loop(save_data_content)

def open_settings():
    settings_menu()

def settings_menu():
    running = True

    # Buttons
    reset_button = Button(250, 250, 300, 50, "Reset Save File", PASTEL_ORANGE, reset_save)
    toggle_controls_button = Button(250, 350, 300, 50, "Toggle Controls", PASTEL_ORANGE, toggle_controls)
    back_button = Button(10, 10, 100, 50, "Back", PASTEL_ORANGE, main_menu)

    buttons = [reset_button, toggle_controls_button, back_button]

    while running:
        screen.fill(PASTEL_YELLOW)
        title = font.render("Settings", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)

        # Show current control scheme
        control_text = f"Current Controls: {current_controls['scheme']}"
        control_surf = font.render(control_text, True, BLACK)
        control_rect = control_surf.get_rect(center=(WIDTH // 2, 200))
        screen.blit(control_surf, control_rect)

        for button in buttons:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(event.pos)

        pygame.display.flip()

def toggle_controls():
    # Toggle between WASD and arrow keys
    if current_controls["scheme"] == "WASD":
        current_controls["scheme"] = "Arrow Keys"
    else:
        current_controls["scheme"] = "WASD"
    print(f"Controls switched to: {current_controls['scheme']}")

def main_menu():
    running = True
    while running:
        screen.fill(PASTEL_YELLOW)

        # Draw title
        title_surf = font.render("Snake Dungeon", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Draw total eggs
        total_eggs_text = f"Total Eggs: {save_data_content['total_eggs']}"
        total_eggs_surf = font.render(total_eggs_text, True, BLACK)
        screen.blit(total_eggs_surf, (WIDTH - 250, 10))

        # Buttons
        buttons = [
            Button(300, 200, 200, 50, "Start Run", GREEN, start_run),
            Button(100, 200, 150, 50, "Store", PASTEL_ORANGE, open_store),
            Button(550, 200, 150, 50, "Gambling", PASTEL_ORANGE, open_gambling),
            Button(10, 10, 100, 50, "Settings", PASTEL_ORANGE, open_settings),
        ]

        for button in buttons:
            button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    button.click(event.pos)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    try:
        print("Starting main menu...")  # Debugging
        main_menu()
    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging
        pygame.quit()