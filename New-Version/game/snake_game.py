import pygame
import random

class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        self.egg_currency = 0
        self.objects = [self.spawn_object() for _ in range(5)]
        self.growth = 1
        self.growth_counter = 0
        self.multiplier = 1
        self.cell_size = 20

    def spawn_object(self):
        return (random.randint(0, self.width // self.cell_size - 1),
                random.randint(0, self.height // self.cell_size - 1))

    def update(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.snake.insert(0, new_head)

        if new_head in self.objects:
            self.objects.remove(new_head)
            self.objects.append(self.spawn_object())
            self.egg_currency += 1 * self.multiplier
            self.growth_counter += 1
        elif self.growth_counter >= self.growth:
            self.growth_counter = 0
        else:
            self.snake.pop()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]: self.direction = (0, -1)
        elif keys[pygame.K_DOWN]: self.direction = (0, 1)
        elif keys[pygame.K_LEFT]: self.direction = (-1, 0)
        elif keys[pygame.K_RIGHT]: self.direction = (1, 0)

    def draw(self, screen):
        for x, y in self.snake:
            pygame.draw.rect(screen, (0, 255, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        for x, y in self.objects:
            pygame.draw.rect(screen, (255, 255, 0), (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Eggs: {self.egg_currency}", True, (255, 255, 255))
        screen.blit(text, (10, 10))