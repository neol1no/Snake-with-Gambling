import pygame
import sys
import random
from save import save_data

def game_loop(data):
    PASTEL_GREEN = (204, 255, 153)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    WIDTH, HEIGHT = 800, 600
    CELL_SIZE = 20

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL_SIZE, 0)

    egg = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
           random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

    run_eggs = 0

    menu_button_rect = pygame.Rect(10, 10, 150, 50)

    running = True
    while running:
        screen.fill(PASTEL_GREEN)

        pygame.draw.rect(screen, WHITE, menu_button_rect)
        menu_text = font.render("Back to Menu", True, BLACK)
        screen.blit(menu_text, (menu_button_rect.centerx - menu_text.get_width() // 2, menu_button_rect.centery - menu_text.get_height() // 2))

        pygame.draw.rect(screen, RED, (*egg, CELL_SIZE, CELL_SIZE))

        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else WHITE
            pygame.draw.rect(screen, color, (*segment, CELL_SIZE, CELL_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data["total_eggs"] += run_eggs
                save_data(data)
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    data["total_eggs"] += run_eggs
                    save_data(data)
                    return
            if event.type == pygame.KEYDOWN:
                controls = data["controls"]
                if (controls == "WASD" and event.key == pygame.K_w) or (controls == "ARROWS" and event.key == pygame.K_UP):
                    if direction != (0, CELL_SIZE):
                        direction = (0, -CELL_SIZE)
                elif (controls == "WASD" and event.key == pygame.K_s) or (controls == "ARROWS" and event.key == pygame.K_DOWN):
                    if direction != (0, -CELL_SIZE):
                        direction = (0, CELL_SIZE)
                elif (controls == "WASD" and event.key == pygame.K_a) or (controls == "ARROWS" and event.key == pygame.K_LEFT):
                    if direction != (CELL_SIZE, 0):
                        direction = (-CELL_SIZE, 0)
                elif (controls == "WASD" and event.key == pygame.K_d) or (controls == "ARROWS" and event.key == pygame.K_RIGHT):
                    if direction != (-CELL_SIZE, 0):
                        direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake = [new_head] + snake[:-1]

        if snake[0] == egg:
            snake.append(snake[-1])
            egg = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                   random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
            run_eggs += 1

        if not (0 <= snake[0][0] < WIDTH and 0 <= snake[0][1] < HEIGHT):
            running = False

        if len(snake) != len(set(snake)):
            running = False

        pygame.display.flip()
        clock.tick(10)

    save_data({"total_eggs": run_eggs, "controls": "WASD"})
    return
