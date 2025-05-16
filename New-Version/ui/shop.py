import pygame

class Shop:
    def __init__(self, game):
        self.game = game
        self.options = [
            ("Grow rate upgrade", 10, self.upgrade_growth),
            ("Currency multiplier", 20, self.upgrade_multiplier),
        ]

    def upgrade_growth(self):
        if self.game.egg_currency >= 10:
            self.game.growth += 1
            self.game.egg_currency -= 10

    def upgrade_multiplier(self):
        if self.game.egg_currency >= 20:
            self.game.multiplier += 1
            self.game.egg_currency -= 20

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: self.options[0][2]()
        if keys[pygame.K_2]: self.options[1][2]()

    def draw(self, screen):
        font = pygame.font.SysFont(None, 36)
        for i, (name, cost, _) in enumerate(self.options):
            text = font.render(f"{i+1}. {name} - {cost} eggs", True, (200, 200, 200))
            screen.blit(text, (100, 100 + i * 40))