import pygame
import sys
import random
import json
import os
from enum import Enum
from sites.shop import Shop
from sites.gambling import Gambling
from sites.settings import Settings
from sites.button import Button

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    SHOP = 3
    GAMBLING = 4
    PAUSE = 5
    SETTINGS = 6
    TRANSITIONING = 7

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        self.previous_state = GameState.MENU
        self.load_save_data()  # Load saved data
        self.upgrades = {
            "grow_rate": 1,
            "currency_multiplier": 1
        }
        self.snake_skin = "default"
        self.shop = Shop(self)
        self.gambling = Gambling(self)
        self.settings = Settings(self)
        self.debug_mode = False
        self.use_arrow_keys = False
        self.setup_buttons()
        self.reset_game()
        self.direction_queue = []
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 100  # 100ms between moves (10 moves per second)
        self.moving_blocks = []
        self.last_moving_block_time = pygame.time.get_ticks()
        self.moving_block_interval = random.randint(1500, 3000)  # 1.5 to 3 seconds
        self.eggs_collected = 0
        self.total_eggs_collected = 0
        
        # Transition variables
        self.transition_alpha = 0
        self.transition_speed = 0.1
        self.transition_surface = pygame.Surface((self.width, self.height))
        self.transition_surface.fill((0, 0, 0))
        self.transition_target = None
        self.transition_start = None

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
            "gambling": Button(center_x, 440, button_width, button_height, "Gambling"),
            "settings": Button(center_x, 510, button_width, button_height, "Settings")
        }
        
        self.pause_buttons = {
            "resume": Button(center_x, 300, button_width, button_height, "Resume"),
            "settings": Button(center_x, 370, button_width, button_height, "Settings"),
            "main_menu": Button(center_x, 440, button_width, button_height, "Main Menu")
        }

        # Add debug toggle button to bottom right
        debug_button_width = 100
        debug_button_height = 30
        self.debug_button = Button(
            self.width - debug_button_width - 20,  # 20px from right edge
            self.height - debug_button_height - 20,  # 20px from bottom
            debug_button_width,
            debug_button_height,
            "Debug: OFF"
        )

    def reset_game(self):
        self.snake = [(self.width//2, self.height//2)]
        self.direction = (20, 0)
        self.direction_queue = []
        self.egg_positions = []
        self.obstacles = []
        self.moving_blocks = []
        self.eggs_collected = 0
        self.total_eggs_collected = 0
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

    def start_transition(self, target_state):
        self.transition_start = self.game_state
        self.transition_target = target_state
        self.game_state = GameState.TRANSITIONING
        self.transition_alpha = 0

    def update_transition(self):
        if self.game_state == GameState.TRANSITIONING:
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 1:
                self.transition_alpha = 1
                self.game_state = self.transition_target
                self.transition_alpha = 0
                self.transition_target = None
                self.transition_start = None

    def draw_transition(self):
        if self.game_state == GameState.TRANSITIONING:
            self.transition_surface.set_alpha(int(self.transition_alpha * 255))
            self.screen.blit(self.transition_surface, (0, 0))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == GameState.PLAYING:
                        self.previous_state = self.game_state
                        self.start_transition(GameState.PAUSE)
                        self.save_data()
                    elif self.game_state == GameState.PAUSE:
                        self.start_transition(GameState.PLAYING)
                    elif self.game_state == GameState.SETTINGS:
                        self.start_transition(self.previous_state)
                    else:
                        self.start_transition(GameState.MENU)
                        self.reset_game()
                        self.gambling.current_game = None
                        self.save_data()
                
                if self.game_state == GameState.PLAYING:
                    # Only add to queue if we have less than 2 directions queued
                    if len(self.direction_queue) < 2:
                        new_direction = None
                        if self.use_arrow_keys:
                            if event.key == pygame.K_UP and self.direction != (0, 20):
                                new_direction = (0, -20)
                            elif event.key == pygame.K_DOWN and self.direction != (0, -20):
                                new_direction = (0, 20)
                            elif event.key == pygame.K_LEFT and self.direction != (20, 0):
                                new_direction = (-20, 0)
                            elif event.key == pygame.K_RIGHT and self.direction != (-20, 0):
                                new_direction = (20, 0)
                        else:
                            if event.key == pygame.K_w and self.direction != (0, 20):
                                new_direction = (0, -20)
                            elif event.key == pygame.K_s and self.direction != (0, -20):
                                new_direction = (0, 20)
                            elif event.key == pygame.K_a and self.direction != (20, 0):
                                new_direction = (-20, 0)
                            elif event.key == pygame.K_d and self.direction != (-20, 0):
                                new_direction = (20, 0)
                        
                        if new_direction is not None:
                            future_direction = self.direction_queue[-1] if self.direction_queue else self.direction
                            if (new_direction[0] != -future_direction[0] or 
                                new_direction[1] != -future_direction[1]):
                                self.direction_queue.append(new_direction)

            if event.type == pygame.MOUSEMOTION:
                if self.game_state == GameState.MENU:
                    for button in self.menu_buttons.values():
                        button.handle_event(event)
                    self.debug_button.handle_event(event)
                elif self.game_state == GameState.PAUSE:
                    for button in self.pause_buttons.values():
                        button.handle_event(event)
                elif self.game_state == GameState.SETTINGS:
                    self.settings.handle_input(event)
                elif self.game_state == GameState.GAMBLING:
                    self.gambling.handle_input(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GameState.MENU:
                    if self.debug_button.handle_event(event):
                        self.debug_mode = not self.debug_mode
                        return
                    
                    for button_name, button in self.menu_buttons.items():
                        if button.handle_event(event):
                            if button_name == "play":
                                self.reset_game()
                                self.start_transition(GameState.PLAYING)
                            elif button_name == "shop":
                                self.start_transition(GameState.SHOP)
                            elif button_name == "gambling":
                                self.gambling.current_game = None
                                self.start_transition(GameState.GAMBLING)
                            elif button_name == "settings":
                                self.previous_state = self.game_state
                                self.start_transition(GameState.SETTINGS)
                
                elif self.game_state == GameState.PAUSE:
                    for button_name, button in self.pause_buttons.items():
                        if button.handle_event(event):
                            if button_name == "resume":
                                self.start_transition(GameState.PLAYING)
                            elif button_name == "settings":
                                self.previous_state = self.game_state
                                self.start_transition(GameState.SETTINGS)
                            elif button_name == "main_menu":
                                self.start_transition(GameState.MENU)
                                self.reset_game()
                                self.gambling.current_game = None
                                self.save_data()
                
                elif self.game_state == GameState.SETTINGS:
                    self.settings.handle_input(event)
                
                elif self.game_state == GameState.SHOP:
                    self.shop.handle_click(pygame.mouse.get_pos())
                elif self.game_state == GameState.GAMBLING:
                    self.gambling.handle_input(event)

    def draw(self):
        self.screen.fill((20, 20, 20))
        
        if self.game_state == GameState.MENU:
            # Draw title with shadow
            title_font = pygame.font.Font(None, 74)
            title_shadow = title_font.render("Snake Game", True, (0, 0, 0))
            title_text = title_font.render("Snake Game", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.width//2, 200))
            self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
            self.screen.blit(title_text, title_rect)
            
            for button in self.menu_buttons.values():
                button.draw(self.screen)
            
            self.debug_button.text = "Debug: ON" if self.debug_mode else "Debug: OFF"
            self.debug_button.draw(self.screen)
        
        elif self.game_state == GameState.PLAYING:
            # Draw grid lines with fade effect
            for x in range(0, self.width, 20):
                pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.height))
            for y in range(0, self.height, 20):
                pygame.draw.line(self.screen, (30, 30, 30), (0, y), (self.width, y))
            
            # Draw snake with gradient effect
            for i, segment in enumerate(self.snake):
                alpha = 255 - (i * 2) if i * 2 < 255 else 0
                color = (0, 255, 0, alpha)
                pygame.draw.rect(self.screen, color, (segment[0], segment[1], 18, 18))
            
            # Draw eggs with glow effect
            for egg in self.egg_positions:
                # Glow
                for radius in range(12, 8, -1):
                    alpha = 100 - (radius * 5)
                    glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (255, 255, 0, alpha), (radius, radius), radius)
                    self.screen.blit(glow_surface, (egg[0] + 10 - radius, egg[1] + 10 - radius))
                # Egg
                pygame.draw.circle(self.screen, (255, 255, 0), (egg[0] + 10, egg[1] + 10), 8)
            
            # Draw obstacles with shadow
            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (200, 0, 0), (obstacle[0] + 2, obstacle[1] + 2, 18, 18))
                pygame.draw.rect(self.screen, (255, 0, 0), (obstacle[0], obstacle[1], 18, 18))
            
            # Draw moving blocks with trail effect
            for block in self.moving_blocks:
                pygame.draw.rect(self.screen, (255, 128, 0), (block['pos'][0], block['pos'][1], 18, 18))
            
            # Draw UI with modern style
            font = pygame.font.Font(None, 36)
            
            # Calculate text widths to size the panel
            length_text = font.render(f"Length: {len(self.snake)}", True, (255, 255, 255))
            score_text = font.render(f"Score: {self.total_eggs_collected}", True, (255, 255, 255))
            eggs_text = font.render(f"Eggs: {self.eggs}", True, (255, 255, 255))
            
            panel_width = max(length_text.get_width(), score_text.get_width(), eggs_text.get_width()) + 40
            panel_height = 120
            
            # Background panel for stats
            panel_rect = pygame.Rect(10, 10, panel_width, panel_height)
            pygame.draw.rect(self.screen, (30, 30, 30), panel_rect, border_radius=10)
            pygame.draw.rect(self.screen, (60, 60, 60), panel_rect, 2, border_radius=10)
            
            # Stats with shadows
            length_shadow = font.render(f"Length: {len(self.snake)}", True, (0, 0, 0))
            score_shadow = font.render(f"Score: {self.total_eggs_collected}", True, (0, 0, 0))
            eggs_shadow = font.render(f"Eggs: {self.eggs}", True, (0, 0, 0))
            
            # Center text in panel
            text_x = 20
            self.screen.blit(length_shadow, (text_x + 2, 22))
            self.screen.blit(score_shadow, (text_x + 2, 57))
            self.screen.blit(eggs_shadow, (text_x + 2, 92))
            
            self.screen.blit(length_text, (text_x, 20))
            self.screen.blit(score_text, (text_x, 55))
            self.screen.blit(eggs_text, (text_x, 90))
        
        elif self.game_state == GameState.PAUSE:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            title_font = pygame.font.Font(None, 74)
            title_shadow = title_font.render("Paused", True, (0, 0, 0))
            title_text = title_font.render("Paused", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.width//2, 200))
            self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
            self.screen.blit(title_text, title_rect)
            
            for button in self.pause_buttons.values():
                button.draw(self.screen)
        
        elif self.game_state == GameState.SETTINGS:
            self.settings.draw(self.screen)
        
        elif self.game_state == GameState.SHOP:
            self.shop.draw(self.screen)
        
        elif self.game_state == GameState.GAMBLING:
            self.gambling.draw(self.screen)
        
        self.draw_transition()
        pygame.display.flip()

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Update transition
        self.update_transition()
        
        if self.game_state == GameState.PLAYING:
            # Update moving blocks
            if current_time - self.last_moving_block_time >= self.moving_block_interval:
                self.last_moving_block_time = current_time
                self.moving_block_interval = random.randint(1500, 3000)
                
                # Create new moving block
                side = random.choice(['top', 'right', 'bottom', 'left'])
                if side == 'top':
                    x = random.randrange(0, self.width, 20)
                    y = 0
                    direction = (0, 20)
                elif side == 'right':
                    x = self.width - 20
                    y = random.randrange(0, self.height, 20)
                    direction = (-20, 0)
                elif side == 'bottom':
                    x = random.randrange(0, self.width, 20)
                    y = self.height - 20
                    direction = (0, -20)
                else:  # left
                    x = 0
                    y = random.randrange(0, self.height, 20)
                    direction = (20, 0)
                
                self.moving_blocks.append({
                    'pos': (x, y),
                    'direction': direction,
                    'last_move': current_time,
                    'move_interval': 1000  # Move every second
                })
            
            # Move existing blocks
            for block in self.moving_blocks[:]:
                if current_time - block['last_move'] >= block['move_interval']:
                    block['last_move'] = current_time
                    new_x = block['pos'][0] + block['direction'][0]
                    new_y = block['pos'][1] + block['direction'][1]
                    
                    # Remove block if it goes off screen
                    if (new_x < 0 or new_x >= self.width or 
                        new_y < 0 or new_y >= self.height):
                        self.moving_blocks.remove(block)
                        continue
                    
                    block['pos'] = (new_x, new_y)
            
            # Check if it's time to move the snake
            if current_time - self.last_move_time >= self.move_interval:
                self.last_move_time = current_time
                
                if self.direction_queue:
                    self.direction = self.direction_queue.pop(0)

                new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
                
                # Check collision with moving blocks
                for block in self.moving_blocks:
                    if new_head == block['pos']:
                        self.start_transition(GameState.MENU)
                        return
                
                if (new_head[0] < 0 or new_head[0] >= self.width or
                    new_head[1] < 0 or new_head[1] >= self.height or
                    new_head in self.snake or new_head in self.obstacles):
                    self.start_transition(GameState.MENU)
                    return

                self.snake.insert(0, new_head)
                
                if new_head in self.egg_positions:
                    self.egg_positions.remove(new_head)
                    self.eggs += self.upgrades["currency_multiplier"]
                    self.eggs_collected += 1
                    self.total_eggs_collected += self.upgrades["currency_multiplier"]
                    if len(self.egg_positions) == 0:
                        self.generate_eggs()
                    if self.eggs_collected >= self.upgrades["grow_rate"]:
                        self.eggs_collected = 0
                    else:
                        self.snake.pop()
                else:
                    self.snake.pop()
        elif self.game_state == GameState.GAMBLING:
            self.gambling.update()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)  # Keep 60 FPS for smooth animations

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 