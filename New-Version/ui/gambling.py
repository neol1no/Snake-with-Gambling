import pygame
import random

class GamblingRoom:
    def __init__(self, game):
        self.game = game
        self.options = [
            ("Slots", self.slots),
            ("Wheel", self.wheel),
            ("Blackjack", self.blackjack),
        ]

    def slots(self):
        if self.game.egg_currency >= 5:
            self.game.egg_currency -= 5
            if random.randint(1, 5) == 1:
                self.game.egg_currency += 20

    def wheel(self):
        if self.game.egg_currency >= 3:
            self.game.egg_currency -= 3
            if random.randint(1, 4) == 1:
                self.game.egg_currency += 12

    def blackjack(self):
        if self.game.egg_currency >= 7:
            self.game.egg_currency -= 7
            if random.randint(1, 2) == 1:
                self.game.egg_currency += 14

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: self.options[0][1]()
        if keys[pygame.K_2]: self.options[1][1]()
        if keys[pygame.K_3]: self.options[2][1]()

    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        for i, (name, _) in enumerate(self.options):
            text = font.render(f"{i+1}. {name}", True, (255, 255, 255))
            screen.blit(text, (100, 100 + i * 40))