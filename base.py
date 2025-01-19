import pygame
import os
import subprocess
from game import game_loop
from save import load_save, save_data, reset_save

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1400, 900
PLAY_AREA = pygame.Rect(int(WIDTH * 0.1), int(HEIGHT * 0.1), int(WIDTH * 0.43), int(HEIGHT * 0.44))
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
font = pygame.font.Font(pygame.font.get_default_font(), int(36 * WIDTH / 1400))  # Adjust font size based on screen width

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
        # Scale position and size based on screen width/height
        self.rect = pygame.Rect(int(x), int(y), int(width), int(height))  # Make sure to pass in pixel values
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

    def open_settings():
        settings_menu()  # Settings-Screen aufrufen

    # Button dimensions and gap
    button_width, button_height = 0.14, 0.06  # Relative sizes
    button_gap = 0.02  # Gap between buttons vertically

    # Convert relative button sizes to pixel values
    button_width_px = int(button_width * WIDTH)
    button_height_px = int(button_height * HEIGHT)
    button_gap_px = int(button_gap * HEIGHT)

    # Calculate total height of all buttons with gaps
    total_button_height_px = 4 * button_height_px + 3 * button_gap_px

    # Calculate starting y-position to center the buttons vertically
    buttons_start_y = (HEIGHT - total_button_height_px) // 2

    # Position buttons horizontally centered and vertically spaced
    buttons = [
        Button((WIDTH - button_width_px) // 2, buttons_start_y, button_width_px, button_height_px, "Start Game", GREEN, start_game),
        Button((WIDTH - button_width_px) // 2, buttons_start_y + (button_height_px + button_gap_px), button_width_px, button_height_px, "Store", ORANGE, open_store),
        Button((WIDTH - button_width_px) // 2, buttons_start_y + 2 * (button_height_px + button_gap_px), button_width_px, button_height_px, "Gambling", ORANGE, open_gambling),
        Button((WIDTH - button_width_px) // 2, buttons_start_y + 3 * (button_height_px + button_gap_px), button_width_px, button_height_px, "Exit", RED, exit)
    ]

    while running:
        screen.fill(PASTEL_YELLOW)
        # Draw title
        title_surf = font.render("Snake Dungeon", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, int(0.06 * HEIGHT)))
        screen.blit(title_surf, title_rect)

        # Draw total eggs
        total_eggs_text = f"Total Eggs: {save_data_content['total_eggs']}"
        total_eggs_surf = font.render(total_eggs_text, True, BLACK)
        screen.blit(total_eggs_surf, (int(0.01 * WIDTH), int(0.01 * HEIGHT)))

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


# Settings menu
def settings_menu():
    running = True

    def reset_game():
        global save_data_content
        save_data(save_data_content)
        print("Save data saved before reset!")
        reset_save()
        print("Save data reset!")
        save_data_content = load_save()
        restart_application()

    def back_to_main_menu():
        restart_application()

    buttons = [
        Button(0.21 * WIDTH, 0.17 * HEIGHT, 0.14 * WIDTH, 0.06 * HEIGHT, "Reset Save", RED, reset_game),
        Button(0.21 * WIDTH, 0.22 * HEIGHT, 0.14 * WIDTH, 0.06 * HEIGHT, "Back to Main Menu", GREEN, back_to_main_menu)
    ]

    while running:
        screen.fill(PASTEL_YELLOW)

        title_surf = font.render("Settings", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, int(0.06 * HEIGHT)))
        screen.blit(title_surf, title_rect)

        for button in buttons:
            button.draw(screen)

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
