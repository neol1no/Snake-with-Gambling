import pygame
import random
import subprocess
from save import save_data

# Game settings
FPS = 15
SNAKE_COLOR = (0, 255, 0)
EGG_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Restart the application
def restart_application(save_data_content):
    save_data(save_data_content)
    pygame.quit()
    subprocess.run(["python", "base.py"])


def game_loop(save_data_content, controls, play_area):
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))

    # Initialize game state
    snake = [(150, 150), (140, 150), (130, 150)]
    snake_dir = (10, 0)
    egg = (random.randint(1, play_area.width // 10 - 1) * 10 + play_area.x,
           random.randint(1, play_area.height // 10 - 1) * 10 + play_area.y)
    score = 0
    snake_length = len(snake)
    start_ticks = pygame.time.get_ticks()
    growth_delay = save_data_content.get("growth_delay", 0)
    growth_counter = 0

    running = True

    # Button for returning to main menu
    class Button:
        def __init__(self, x, y, width, height, text, color, action=None):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = color
            self.action = action

        def draw(self, screen):
            pygame.draw.rect(screen, self.color, self.rect)
            text_surf = pygame.font.Font(None, 36).render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def click(self, pos):
            if self.rect.collidepoint(pos) and self.action:
                self.action()

    back_button = Button(10, 550, 200, 50, "Back to Menu", (255, 100, 100), lambda: restart_application(save_data_content))

    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, (200, 200, 200), play_area, 2)

        # Draw the snake
        for segment in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (*segment, 10, 10))
        
        # Draw the egg
        pygame.draw.rect(screen, EGG_COLOR, (*egg, 10, 10))

        # Timer
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = pygame.font.Font(None, 36).render(f"Time: {elapsed_time}s", True, BLACK)
        screen.blit(timer_text, (600, 10))

        # Collected eggs
        collected_text = pygame.font.Font(None, 36).render(f"Eggs: {score}", True, BLACK)
        screen.blit(collected_text, (600, 50))

        # Snake length
        length_text = pygame.font.Font(None, 36).render(f"Length: {len(snake)}", True, BLACK)
        screen.blit(length_text, (600, 90))

        # Draw the back button
        back_button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data_content['total_eggs'] += score
                save_data(save_data_content)
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                back_button.click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if controls["scheme"] == "WASD":
                    if event.key == pygame.K_w and snake_dir != (0, 10):
                        snake_dir = (0, -10)
                    elif event.key == pygame.K_s and snake_dir != (0, -10):
                        snake_dir = (0, 10)
                    elif event.key == pygame.K_a and snake_dir != (10, 0):
                        snake_dir = (-10, 0)
                    elif event.key == pygame.K_d and snake_dir != (-10, 0):
                        snake_dir = (10, 0)

        # Move snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
        snake = [new_head] + snake[:-1]

        # Check collisions
        if new_head in snake[1:] or not play_area.contains(pygame.Rect(*new_head, 10, 10)):
            save_data_content['total_eggs'] += score
            save_data(save_data_content)
            break

        # Check if snake eats egg
        if new_head == egg:
            score += 1 * (save_data_content.get("eggs_per_level", 1))  # Apply multiplier
            growth_counter += 1
            if growth_counter >= growth_delay + 1:  # Apply growth delay
                snake.append(snake[-1])
                growth_counter = 0
            egg = (random.randint(1, play_area.width // 10 - 1) * 10 + play_area.x,
                   random.randint(1, play_area.height // 10 - 1) * 10 + play_area.y)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
