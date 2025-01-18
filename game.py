import pygame
import random
import time
from save import load_save, save_data, reset_save

# Game settings
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (255, 253, 208)
SNAKE_COLOR = (0, 255, 0)
EGG_COLOR = (255, 255, 0)
FPS = 15

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Dungeon")

# Fonts
font = pygame.font.Font(pygame.font.get_default_font(), 36)

# Game state variables
snake = [(100, 100), (90, 100), (80, 100)]  # Initial snake position
snake_dir = (10, 0)  # Snake direction (moving right initially)
current_collected_eggs = 0
start_ticks = pygame.time.get_ticks()  # Start time for the timer

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], 10, 10))

def move_snake():
    global snake
    head_x, head_y = snake[0]
    new_head = (head_x + snake_dir[0], head_y + snake_dir[1])
    snake = [new_head] + snake[:-1]

def check_collision():
    head_x, head_y = snake[0]
    # Collision with wall
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        return True
    # Collision with self (body)
    if (head_x, head_y) in snake[1:]:
        return True
    return False

def spawn_egg():
    egg_x = random.randint(0, (WIDTH - 10) // 10) * 10
    egg_y = random.randint(0, (HEIGHT - 10) // 10) * 10
    return egg_x, egg_y

def back_to_menu(save_data_content, current_collected_eggs):
    save_data_content['total_eggs'] += current_collected_eggs
    save_data(save_data_content)  # Save the updated data
    pygame.quit()
    import base
    base.main_menu()

def game_loop(save_data_content, current_controls):
    global snake, snake_dir, current_collected_eggs, start_ticks

    egg_x, egg_y = spawn_egg()
    running = True
    clock = pygame.time.Clock()

    # Back to Menu Button
    back_button = pygame.Rect(10, HEIGHT - 60, 150, 50)

    while running:
        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if current_controls["scheme"] == "WASD":
                    if event.key == pygame.K_w and snake_dir != (0, 10):
                        snake_dir = (0, -10)
                    elif event.key == pygame.K_s and snake_dir != (0, -10):
                        snake_dir = (0, 10)
                    elif event.key == pygame.K_a and snake_dir != (10, 0):
                        snake_dir = (-10, 0)
                    elif event.key == pygame.K_d and snake_dir != (-10, 0):
                        snake_dir = (10, 0)
                elif current_controls["scheme"] == "Arrow Keys":
                    if event.key == pygame.K_LEFT and snake_dir != (10, 0):
                        snake_dir = (-10, 0)
                    elif event.key == pygame.K_RIGHT and snake_dir != (-10, 0):
                        snake_dir = (10, 0)
                    elif event.key == pygame.K_UP and snake_dir != (0, 10):
                        snake_dir = (0, -10)
                    elif event.key == pygame.K_DOWN and snake_dir != (0, -10):
                        snake_dir = (0, 10)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    back_to_menu(save_data_content, current_collected_eggs)

        move_snake()

        # Check for collisions
        if check_collision():
            print(f"Game Over! Total Eggs Collected: {current_collected_eggs}")
            back_to_menu(save_data_content, current_collected_eggs)

        # Collect egg if eaten
        head_x, head_y = snake[0]
        if head_x == egg_x and head_y == egg_y:
            egg_x, egg_y = spawn_egg()
            snake.append(snake[-1])  # Add new segment
            current_collected_eggs += 1

        draw_snake()

        # Draw egg
        pygame.draw.rect(screen, EGG_COLOR, (egg_x, egg_y, 10, 10))

        # Draw timer
        elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
        timer_text = f"Time: {elapsed_time}s"
        timer_surf = font.render(timer_text, True, (0, 0, 0))
        screen.blit(timer_surf, (WIDTH - 150, 10))

        # Draw total eggs collected
        egg_text = f"Eggs: {current_collected_eggs}"
        egg_surf = font.render(egg_text, True, (0, 0, 0))
        screen.blit(egg_surf, (WIDTH - 150, 50))

        # Draw back button
        pygame.draw.rect(screen, (255, 200, 124), back_button)
        back_text = font.render("Back to Menu", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)

        # Update the display
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()