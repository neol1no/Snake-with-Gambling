import pygame
import random  # <-- Make sure random is imported
import subprocess
from save import save_data

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gambling Games")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
RED = (255, 0, 0)
PASTEL_ORANGE = (255, 200, 124)

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)


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


# Gambling menu
def gambling_menu(save_data_content):
    running = True

    def slot_machine():
        slot_machine_logic(save_data_content)

    def plinko():
        plinko_logic(save_data_content)

    def roulette():
        roulette_logic(save_data_content)

    def back_to_menu():
        restart_application(save_data_content)

    buttons = [
        Button(300, 150, 200, 50, "Slot Machine", GREEN, slot_machine),
        Button(300, 250, 200, 50, "Plinko", PASTEL_ORANGE, plinko),
        Button(300, 350, 200, 50, "Roulette", PASTEL_ORANGE, roulette),
        Button(300, 450, 200, 50, "Back to Menu", RED, back_to_menu),
    ]

    while running:
        screen.fill(WHITE)

        # Draw title
        title_surf = font.render("Gambling Games", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title_surf, title_rect)

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


# Slot Machine Logic
def slot_machine_logic(save_data_content):
    running = True
    current_bet = 10
    colors = ["red", "green", "blue"]
    slot_result = [random.choice(colors) for _ in range(3)]  # Initiale gültige Werte

    def increase_bet():
        nonlocal current_bet
        if save_data_content['total_eggs'] > current_bet:
            current_bet += 10

    def decrease_bet():
        nonlocal current_bet
        if current_bet > 10:
            current_bet -= 10

    def spin():
        nonlocal slot_result
        if save_data_content['total_eggs'] < current_bet:
            print("Not enough eggs!")
            return

        save_data_content['total_eggs'] -= current_bet
        save_data(save_data_content)

        # Simulate spinning animation
        for _ in range(15):  # Number of animation frames
            slot_result = [random.choice(colors) for _ in range(3)]
            screen.fill(WHITE)
            display_slots(slot_result)
            pygame.display.flip()
            pygame.time.wait(100)  # Wait 100ms between frames

        # Final result
        slot_result = [random.choice(colors) for _ in range(3)]
        if len(set(slot_result)) == 1:  # All colors match
            winnings = current_bet * 3
            save_data_content['total_eggs'] += winnings
            print(f"You WON! +{winnings} eggs.")
        else:
            print(f"You lost! Result: {slot_result}")
        save_data(save_data_content)

    # Helper function to display the slots
    def display_slots(slot_result):
        color_map = {
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
        }
        for i, color in enumerate(slot_result):
            if color not in color_map:
                raise ValueError(f"Invalid color name: {color}")  # Fehlerbehandlung
            pygame.draw.rect(screen, color_map[color], (200 + i * 100, 200, 80, 80))  # Slot rectangles
            text = font.render(color.upper(), True, BLACK)
            text_rect = text.get_rect(center=(240 + i * 100, 240))
            screen.blit(text, text_rect)

    # Buttons
    increase_bet_button = Button(500, 400, 100, 50, "+ Bet", GREEN, increase_bet)
    decrease_bet_button = Button(200, 400, 100, 50, "- Bet", RED, decrease_bet)
    spin_button = Button(350, 500, 100, 50, "SPIN", PASTEL_ORANGE, spin)
    back_button = Button(10, 550, 150, 50, "Back", RED, lambda: restart_application(save_data_content))

    while running:
        screen.fill(WHITE)

        # Title
        title_surf = font.render("Slot Machine", True, BLACK)
        screen.blit(title_surf, (WIDTH // 2 - 100, 50))

        # Current bet
        bet_text = font.render(f"Bet: {current_bet}", True, BLACK)
        screen.blit(bet_text, (350, 100))

        # Display the slot result
        display_slots(slot_result)

        # Draw buttons
        for button in [increase_bet_button, decrease_bet_button, spin_button, back_button]:
            button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in [increase_bet_button, decrease_bet_button, spin_button, back_button]:
                    button.click(event.pos)

        pygame.display.flip()

# Plinko Logic (Placeholder)
def plinko_logic(save_data_content):
    print("Plinko coming soon!")


# Roulette Logic (Placeholder)
def roulette_logic(save_data_content):
    print("Roulette coming soon!")
