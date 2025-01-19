import pygame
import subprocess
from save import save_data

# Store settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Dungeon Store")

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PASTEL_ORANGE = (255, 200, 124)


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
        cost = 10 * (2 ** level)
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
        cost = 15 * (2 ** level)
        if save_data_content['total_eggs'] >= cost:
            save_data_content['total_eggs'] -= cost
            save_data_content['growth_delay'] = level + 1
            save_data(save_data_content)
            print(f"Growth Delay upgraded to level {level + 1}.")
        else:
            print("Not enough eggs to upgrade!")

    def back_to_menu():
        restart_application(save_data_content)

    buttons = [
        Button(300, 150, 200, 50, "Upgrade Egg Multiplier", GREEN, upgrade_eggs),
        Button(300, 250, 200, 50, "Upgrade Growth Delay", PASTEL_ORANGE, upgrade_growth),
        Button(300, 350, 200, 50, "Back to Menu", RED, back_to_menu),
    ]

    while running:
        screen.fill(WHITE)

        # Title
        title_surf = font.render("Store", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surf, title_rect)

        # Current eggs display
        egg_count_text = f"Current Eggs: {save_data_content['total_eggs']}"
        egg_count_surf = font.render(egg_count_text, True, BLACK)
        screen.blit(egg_count_surf, (10, 10))

        # Upgrade details
        egg_multiplier_level = save_data_content.get('egg_multiplier', 0)
        egg_multiplier_cost = 5 * (2 ** egg_multiplier_level)
        egg_multiplier_info = f"Level: {egg_multiplier_level}, Cost: {egg_multiplier_cost}"
        egg_multiplier_surf = font.render(egg_multiplier_info, True, BLACK)
        screen.blit(egg_multiplier_surf, (300, 210))

        growth_delay_level = save_data_content.get('growth_delay', 0)
        growth_delay_cost = 10 * (2 ** growth_delay_level)
        growth_delay_info = f"Level: {growth_delay_level}, Cost: {growth_delay_cost}"
        growth_delay_surf = font.render(growth_delay_info, True, BLACK)
        screen.blit(growth_delay_surf, (300, 310))

        # Draw buttons
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
