import pygame
import subprocess
import tkinter as tk
from save import save_data

# Store settings
root = tk.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
root.destroy()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Dungeon Store")

# Adjust font size dynamically based on screen width
font_size = int(36 * WIDTH / 1400)  # Scale font size based on screen width
font = pygame.font.Font(pygame.font.get_default_font(), font_size)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PASTEL_ORANGE = (255, 200, 124)


# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, action=None):
        # Adjust position and size based on screen width/height
        self.rect = pygame.Rect(int(x * WIDTH), int(y * HEIGHT), int(width * WIDTH), int(height * HEIGHT))
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


# Restart the application
def restart_application(save_data_content):
    save_data(save_data_content)  # Save current progress
    pygame.quit()
    subprocess.run(["python", "base.py"])  # Restart base.py


# Store loop
def store_loop(save_data_content):
    running = True

    def upgrade_eggs():
        level = save_data_content.get('egg_multiplier', 0)
        cost = 5 * (2 ** level)
        eggs_per_level = 2 ** (level + 1)
        if save_data_content['total_eggs'] >= cost:
            save_data_content['total_eggs'] -= cost
            save_data_content['egg_multiplier'] = level + 1
            save_data_content['eggs_per_level'] = eggs_per_level
            save_data(save_data_content)
            print(f"Egg Multiplier upgraded to level {level + 1}. You now get {eggs_per_level} eggs per level.")
        else:
            print("Not enough eggs to upgrade!")

    def upgrade_growth():
        level = save_data_content.get('growth_delay', 0)
        cost = 10 * (2 ** level)
        if save_data_content['total_eggs'] >= cost:
            save_data_content['total_eggs'] -= cost
            save_data_content['growth_delay'] = level + 1
            save_data(save_data_content)
            print(f"Growth Delay upgraded to level {level + 1}.")
        else:
            print("Not enough eggs to upgrade!")

    def back_to_menu():
        restart_application(save_data_content)


    button_width, button_height = 0.14, 0.06  
    button_gap = 0.02  
    button_width_px = int(button_width * WIDTH)
    button_height_px = int(button_height * HEIGHT)
    button_gap_px = int(button_gap * HEIGHT)

# Define buttons list before calculating total_button_height_px
    buttons = [
    Button(0, 0, button_width, button_height, "Upgrade Egg Multiplier", GREEN, upgrade_eggs),
    Button(0, 0, button_width, button_height, "Upgrade Growth Delay", PASTEL_ORANGE, upgrade_growth),
    Button(0, 0, button_width, button_height, "Back to Menu", RED, back_to_menu),
    ]

    total_button_height_px = len(buttons) * button_height_px + (len(buttons) - 1) * button_gap_px
    buttons_start_y = (HEIGHT - total_button_height_px) // 2

# Update button positions with relative positioning based on the screen size
    buttons[0].rect.topleft = ((WIDTH - button_width_px) // 2, buttons_start_y)
    buttons[1].rect.topleft = ((WIDTH - button_width_px) // 2, buttons_start_y + button_height_px + button_gap_px)
    buttons[2].rect.topleft = ((WIDTH - button_width_px) // 2, buttons_start_y + 2 * (button_height_px + button_gap_px))

    while running:
        screen.fill(WHITE)

        # Title with dynamic positioning
        title_surf = font.render("Store", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, int(0.1 * HEIGHT)))
        screen.blit(title_surf, title_rect)

        # Current eggs display with dynamic placement
        egg_count_text = f"Current Eggs: {save_data_content['total_eggs']}"
        egg_count_surf = font.render(egg_count_text, True, BLACK)
        screen.blit(egg_count_surf, (int(0.01 * WIDTH), int(0.01 * HEIGHT)))

        # Upgrade details with dynamic positioning
        egg_multiplier_level = save_data_content.get('egg_multiplier', 0)
        egg_multiplier_cost = 5 * (2 ** egg_multiplier_level)
        egg_multiplier_info = f"Level: {egg_multiplier_level}, Cost: {egg_multiplier_cost}"
        egg_multiplier_surf = font.render(egg_multiplier_info, True, BLACK)
        screen.blit(egg_multiplier_surf, (int(0.21 * WIDTH), int(0.21 * HEIGHT)))

        growth_delay_level = save_data_content.get('growth_delay', 0)
        growth_delay_cost = 10 * (2 ** growth_delay_level)
        growth_delay_info = f"Level: {growth_delay_level}, Cost: {growth_delay_cost}"
        growth_delay_surf = font.render(growth_delay_info, True, BLACK)
        screen.blit(growth_delay_surf, (int(0.21 * WIDTH), int(0.31 * HEIGHT)))

        # Draw buttons
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
