import pygame
import random
import subprocess
from save import save_data

# Screen settings
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gambling Games")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (144, 238, 144)
RED = (255, 0, 0)
PASTEL_ORANGE = (255, 200, 124)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Game Variables
wheel_colors = ['red', 'black', 'green']
wheel_positions = random.choices(wheel_colors, k=12)

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


# Responsive UI function for displaying dynamic messages
def display_message(message, y_pos):
    message_surf = font.render(message, True, RED)
    message_rect = message_surf.get_rect(center=(WIDTH // 2, y_pos))
    screen.blit(message_surf, message_rect)


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
    slot_result = [random.choice(colors) for _ in range(3)]

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
            display_message("Not enough eggs!", 400)
            return

        save_data_content['total_eggs'] -= current_bet
        save_data(save_data_content)

        # Simulate spinning animation
        for _ in range(15):
            slot_result = [random.choice(colors) for _ in range(3)]
            screen.fill(WHITE)
            display_slots(slot_result)
            pygame.display.flip()
            pygame.time.wait(100)

        # Final result
        slot_result = [random.choice(colors) for _ in range(3)]
        if len(set(slot_result)) == 1:
            winnings = current_bet * 3
            save_data_content['total_eggs'] += winnings
            display_message(f"You WON! +{winnings} eggs.", 500)
        else:
            display_message(f"You lost! Result: {slot_result}", 500)
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
                raise ValueError(f"Invalid color name: {color}")
            pygame.draw.rect(screen, color_map[color], (200 + i * 100, 200, 80, 80))
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


# Plinko logic
def plinko_logic(save_data_content):
    running = True
    num_balls = 1
    eggs_per_ball = 10
    multipliers = [0.5, 1, 2, 5, 10]
    pegs = []
    ball_positions = []
    
    num_rows = 10
    for row in range(num_rows):
        num_pegs = row + 1
        start_x = (WIDTH - num_pegs * 60) // 2
        for col in range(num_pegs):
            peg_x = start_x + col * 60
            peg_y = 50 + row * 60
            pegs.append((peg_x, peg_y))

    def increase_balls():
        nonlocal num_balls
        num_balls += 1

    def decrease_balls():
        nonlocal num_balls
        if num_balls > 1:
            num_balls -= 1

    def increase_eggs():
        nonlocal eggs_per_ball
        eggs_per_ball += 1

    def decrease_eggs():
        nonlocal eggs_per_ball
        if eggs_per_ball > 1:
            eggs_per_ball -= 1

    def start_plinko():
        nonlocal num_balls, eggs_per_ball
        if save_data_content['total_eggs'] < num_balls * eggs_per_ball:
            display_message("Not enough eggs!", 400)
            return

        save_data_content['total_eggs'] -= num_balls * eggs_per_ball
        save_data(save_data_content)

        total_winnings = 0
        for _ in range(num_balls):
            ball_position = WIDTH // 2
            current_y = 50
            direction = 0

            for row in range(1, num_rows):
                current_y += 60
                if random.random() < 0.7:
                    direction = 0
                else:
                    direction = random.choice([-1, 1])

                ball_position += direction * 60
                ball_position = max(100, min(ball_position, WIDTH - 100))

            multiplier = random.choice(multipliers)
            total_winnings += eggs_per_ball * multiplier

        save_data_content['total_eggs'] += total_winnings
        display_message(f"You won {total_winnings} eggs!", 500)

        save_data(save_data_content)

    # Buttons for balls and eggs
    increase_balls_button = Button(500, 400, 100, 50, "+ Balls", PASTEL_ORANGE, increase_balls)
    decrease_balls_button = Button(200, 400, 100, 50, "- Balls", PASTEL_ORANGE, decrease_balls)
    increase_eggs_button = Button(500, 500, 100, 50, "+ Eggs", PASTEL_ORANGE, increase_eggs)
    decrease_eggs_button = Button(200, 500, 100, 50, "- Eggs", PASTEL_ORANGE, decrease_eggs)

    start_button = Button(350, 550, 100, 50, "START", PASTEL_ORANGE, start_plinko)

    while running:
        screen.fill(WHITE)

        for peg in pegs:
            pygame.draw.circle(screen, BLACK, peg, 5)

        for i, multiplier in enumerate(multipliers):
            pygame.draw.rect(screen, BLACK, (100 + i * 120, 500, 100, 50))
            multiplier_text = font.render(f"x{multiplier}", True, WHITE)
            screen.blit(multiplier_text, (100 + i * 120 + 30, 510))

        ball_text = font.render(f"Balls: {num_balls}", True, BLACK)
        screen.blit(ball_text, (350, 50))
        egg_text = font.render(f"Eggs per Ball: {eggs_per_ball}", True, BLACK)
        screen.blit(egg_text, (350, 100))

        total_eggs_text = f"Total Eggs: {save_data_content['total_eggs']}"
        total_eggs_surf = font.render(total_eggs_text, True, BLACK)
        screen.blit(total_eggs_surf, (350, 150))

        for button in [increase_balls_button, decrease_balls_button, increase_eggs_button, decrease_eggs_button, start_button]:
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in [increase_balls_button, decrease_balls_button, increase_eggs_button, decrease_eggs_button, start_button]:
                    button.click(event.pos)

        pygame.display.flip()

    pygame.quit()


# Roulette Logic
def roulette_logic(save_data_content):
    running = True
    current_bet = 10
    bet_color = "red"
    bet_number = 0

    def increase_bet():
        nonlocal current_bet
        if save_data_content['total_eggs'] > current_bet:
            current_bet += 10

    def decrease_bet():
        nonlocal current_bet
        if current_bet > 10:
            current_bet -= 10

    def spin():
        nonlocal bet_color, bet_number
        if save_data_content['total_eggs'] < current_bet:
            display_message("Not enough eggs!", 400)
            return

        save_data_content['total_eggs'] -= current_bet
        save_data(save_data_content)

        result_number = random.randint(0, 36)
        result_color = wheel_colors[result_number % len(wheel_colors)]

        # Winning logic
        winnings = 0
        if result_color == bet_color:
            winnings = current_bet * 2
        elif result_number == bet_number:
            winnings = current_bet * 35

        if winnings > 0:
            save_data_content['total_eggs'] += winnings
            display_message(f"You won {winnings} eggs!", 500)
        else:
            display_message(f"You lost! Result: {result_number} ({result_color})", 500)

        save_data(save_data_content)

    # Buttons for betting
    increase_bet_button = Button(500, 400, 100, 50, "+ Bet", GREEN, increase_bet)
    decrease_bet_button = Button(200, 400, 100, 50, "- Bet", RED, decrease_bet)
    spin_button = Button(350, 500, 100, 50, "SPIN", PASTEL_ORANGE, spin)
    back_button = Button(10, 550, 150, 50, "Back", RED, lambda: restart_application(save_data_content))

    while running:
        screen.fill(WHITE)

        # Title
        title_surf = font.render("Roulette", True, BLACK)
        screen.blit(title_surf, (WIDTH // 2 - 100, 50))

        # Current bet
        bet_text = font.render(f"Bet: {current_bet}", True, BLACK)
        screen.blit(bet_text, (350, 100))

        # Draw the wheel
        wheel_text = font.render(f"Wheel: {bet_number} ({bet_color})", True, BLACK)
        screen.blit(wheel_text, (350, 150))

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
