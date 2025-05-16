import pygame
import sys
import random
import json
import os
from enum import Enum
from shop import Shop
from gambling import Gambling

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    SHOP = 3
    GAMBLING = 4
    PAUSE = 5

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        self.load_save_data()  # Load saved data
        self.upgrades = {
            "grow_rate": 1,
            "currency_multiplier": 1
        }
        self.snake_skin = "default"
        self.shop = Shop(self)
        self.gambling = Gambling(self)
        self.setup_buttons()
        self.reset_game()
        self.direction_queue = []
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 100  # 100ms between moves (10 moves per second)

    def load_save_data(self):
        try:
            if os.path.exists('save_data.json'):
                with open('save_data.json', 'r') as f:
                    data = json.load(f)
                    self.eggs = data.get('eggs', 0)
            else:
                self.eggs = 0
        except Exception as e:
            print(f"Error loading save data: {e}")
            self.eggs = 0

    def save_data(self):
        try:
            data = {
                'eggs': self.eggs
            }
            with open('save_data.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.width // 2 - button_width // 2
        
        self.menu_buttons = {
            "play": Button(center_x, 300, button_width, button_height, "Play"),
            "shop": Button(center_x, 370, button_width, button_height, "Shop"),
            "gambling": Button(center_x, 440, button_width, button_height, "Gambling")
        }
        
        self.pause_buttons = {
            "resume": Button(center_x, 300, button_width, button_height, "Resume"),
            "settings": Button(center_x, 370, button_width, button_height, "Settings"),
            "main_menu": Button(center_x, 440, button_width, button_height, "Main Menu")
        }

    def reset_game(self):
        self.snake = [(self.width//2, self.height//2)]
        self.direction = (20, 0)
        self.direction_queue = []  # Reset direction queue
        self.egg_positions = []
        self.obstacles = []
        self.generate_obstacles()
        self.generate_eggs()

    def generate_obstacles(self):
        self.obstacles = []
        for _ in range(10):
            x = random.randrange(0, self.width, 20)
            y = random.randrange(0, self.height, 20)
            self.obstacles.append((x, y))

    def generate_eggs(self):
        self.egg_positions = []
        for _ in range(5):
            while True:
                x = random.randrange(0, self.width, 20)
                y = random.randrange(0, self.height, 20)
                if (x, y) not in self.obstacles and (x, y) not in self.snake:
                    self.egg_positions.append((x, y))
                    break

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.game_state = GameState.PAUSE
                        self.save_data()
                    elif self.game_state == GameState.PAUSE:
                        self.game_state = GameState.PLAYING
                    else:
                        self.game_state = GameState.MENU
                        self.reset_game()
                        self.gambling.current_game = None
                        self.save_data()
                
                if self.game_state == GameState.PLAYING:
                    # Only add to queue if we have less than 2 directions queued
                    if len(self.direction_queue) < 2:
                        new_direction = None
                        if event.key == pygame.K_w and self.direction != (0, 20):
                            new_direction = (0, -20)
                        elif event.key == pygame.K_s and self.direction != (0, -20):
                            new_direction = (0, 20)
                        elif event.key == pygame.K_a and self.direction != (20, 0):
                            new_direction = (-20, 0)
                        elif event.key == pygame.K_d and self.direction != (-20, 0):
                            new_direction = (20, 0)
                        
                        if new_direction is not None:
                            # Get the direction we'll be moving in at the time this queued direction is executed
                            # If queue is empty, it's the current direction, otherwise it's the last queued direction
                            future_direction = self.direction_queue[-1] if self.direction_queue else self.direction
                            
                            # Only queue if the new direction isn't opposite to the future direction
                            if (new_direction[0] != -future_direction[0] or 
                                new_direction[1] != -future_direction[1]):
                                self.direction_queue.append(new_direction)

            if event.type == pygame.MOUSEMOTION:
                if self.game_state == GameState.MENU:
                    for button in self.menu_buttons.values():
                        button.handle_event(event)
                elif self.game_state == GameState.PAUSE:
                    for button in self.pause_buttons.values():
                        button.handle_event(event)
                elif self.game_state == GameState.GAMBLING:
                    self.gambling.handle_mouse_motion(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GameState.MENU:
                    for button_name, button in self.menu_buttons.items():
                        if button.handle_event(event):
                            if button_name == "play":
                                self.reset_game()
                                self.game_state = GameState.PLAYING
                            elif button_name == "shop":
                                self.game_state = GameState.SHOP
                            elif button_name == "gambling":
                                self.gambling.current_game = None
                                self.game_state = GameState.GAMBLING
                
                elif self.game_state == GameState.PAUSE:
                    for button_name, button in self.pause_buttons.items():
                        if button.handle_event(event):
                            if button_name == "resume":
                                self.game_state = GameState.PLAYING
                            elif button_name == "main_menu":
                                self.game_state = GameState.MENU
                                self.reset_game()
                                self.gambling.current_game = None
                                self.save_data()  # Save when returning to menu
                
                elif self.game_state == GameState.SHOP:
                    self.shop.handle_click(pygame.mouse.get_pos())
                elif self.game_state == GameState.GAMBLING:
                    self.gambling.handle_input(event)

    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.game_state == GameState.PLAYING:
            # Check if it's time to move the snake
            if current_time - self.last_move_time >= self.move_interval:
                self.last_move_time = current_time
                
                # Apply next direction from queue if available
                if self.direction_queue:
                    self.direction = self.direction_queue.pop(0)

                new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
                
                if (new_head[0] < 0 or new_head[0] >= self.width or
                    new_head[1] < 0 or new_head[1] >= self.height or
                    new_head in self.snake or new_head in self.obstacles):
                    self.game_state = GameState.MENU
                    return

                self.snake.insert(0, new_head)
                
                if new_head in self.egg_positions:
                    self.egg_positions.remove(new_head)
                    self.eggs += self.upgrades["currency_multiplier"]
                    if len(self.egg_positions) == 0:
                        self.generate_eggs()
                else:
                    self.snake.pop()
        elif self.game_state == GameState.GAMBLING:
            self.gambling.update()

    def draw(self):
        self.screen.fill((20, 20, 20))
        
        if self.game_state == GameState.PLAYING:
            for segment in self.snake:
                color = self.shop.skins[self.snake_skin]["color"]
                if color is None:  # Rainbow skin
                    hue = (pygame.time.get_ticks() % 360) / 360
                    color = pygame.Color(0, 0, 0)
                    color.hsva = (hue * 360, 100, 100, 100)
                pygame.draw.rect(self.screen, color, (segment[0], segment[1], 18, 18))
            
            for egg in self.egg_positions:
                pygame.draw.ellipse(self.screen, (255, 255, 0), (egg[0], egg[1], 18, 18))
            
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (255, 0, 0), (obstacle[0], obstacle[1], 18, 18))
            
            font = pygame.font.Font(None, 36)
            eggs_text = font.render(f"Eggs: {self.eggs}", True, (255, 255, 255))
            self.screen.blit(eggs_text, (10, 10))
        
        elif self.game_state == GameState.MENU:
            font = pygame.font.Font(None, 74)
            title = font.render("Snake Game", True, (255, 255, 255))
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 200))
            
            for button in self.menu_buttons.values():
                button.draw(self.screen)
        
        elif self.game_state == GameState.PAUSE:
            font = pygame.font.Font(None, 74)
            title = font.render("Paused", True, (255, 255, 255))
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 200))
            
            for button in self.pause_buttons.values():
                button.draw(self.screen)
        
        elif self.game_state == GameState.SHOP:
            self.shop.draw(self.screen)
        
        elif self.game_state == GameState.GAMBLING:
            self.gambling.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)  # Keep 60 FPS for smooth animations

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 