import pygame
import sys
from game.snake_game import SnakeGame
from ui.shop import Shop
from ui.gambling import GamblingRoom

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Egg Snake")

clock = pygame.time.Clock()
game = SnakeGame(SCREEN_WIDTH, SCREEN_HEIGHT)
shop = Shop(game)
gambling = GamblingRoom(game)

state = "game"

while True:
    screen.fill((30, 30, 30))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                state = "game"
            elif event.key == pygame.K_2:
                state = "shop"
            elif event.key == pygame.K_3:
                state = "gamble"

    if state == "game":
        game.update()
        game.draw(screen)
    elif state == "shop":
        shop.update()
        shop.draw(screen)
    elif state == "gamble":
        gambling.update()
        gambling.draw(screen)

    pygame.display.flip()
    clock.tick(60)