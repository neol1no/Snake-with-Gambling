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
        self.width = 1260
        self.height = 720
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.display_width, self.display_height = self.screen.get_size()
        self.scale_x = self.display_width / self.width
        self.scale_y = self.display_height / self.height
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        self.previous_state = GameState.MENU
        self.load_save_data()
        self.upgrades = {
            "grow_rate": 1,
            "currency_multiplier": 1,
            "egg_magnet": 0,
            "golden_egg_chance": 0
        }
        self.snake_skin = "default"
        self.owned_skins = {"default"}
        self.shop = Shop(self)
        self.gambling = Gambling(self)
        self.settings = Settings(self)
        self.debug_mode = False
        self.use_arrow_keys = False
        self.setup_buttons()
        self.load_assets()
        self.reset_game()
        self.direction_queue = []
        self.last_move_time = pygame.time.get_ticks()
        self.move_interval = 100
        self.moving_blocks = []
        self.last_moving_block_time = pygame.time.get_ticks()
        self.moving_block_interval = random.randint(1500, 3000)
        self.eggs_collected = 0
        self.total_eggs_collected = 0
        self.showing_death_summary = False
        self.death_summary_time = 0
        self.death_menu_button = Button(self.width//2 - 100, self.height//2 + 100, 200, 50, "Main Menu", self)
        
        self.transition_alpha = 0
        self.transition_speed = 0.1
        self.transition_surface = pygame.Surface((self.display_width, self.display_height))
        self.transition_surface.fill((0, 0, 0))
        self.transition_target = None
        self.transition_start = None

    def load_save_data(self):
        self.eggs = 0
        if os.path.exists('save_data.json'):
            try:
                with open('save_data.json', 'r') as f:
                    data = json.load(f)
                    self.eggs = data.get('eggs', 0)
            except Exception as e:
                print(f"Error loading save data: {e}")

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
            "play": Button(center_x, 300, button_width, button_height, "Play", self),
            "shop": Button(center_x, 370, button_width, button_height, "Shop", self),
            "gambling": Button(center_x, 440, button_width, button_height, "Gambling", self),
            "settings": Button(center_x, 510, button_width, button_height, "Settings", self)
        }
        
        self.pause_buttons = {
            "resume": Button(center_x, 300, button_width, button_height, "Resume", self),
            "settings": Button(center_x, 370, button_width, button_height, "Settings", self),
            "main_menu": Button(center_x, 440, button_width, button_height, "Main Menu", self)
        }

        debug_button_width = 100
        debug_button_height = 30
        self.debug_button = Button(
            self.width - debug_button_width - 20,  
            self.height - debug_button_height - 20,  
            debug_button_width,
            debug_button_height,
            "Debug: OFF",
            self
        )

        
        exit_button_width = 40
        exit_button_height = 40
        self.exit_button = Button(
            self.width - exit_button_width - 20,
            20, 
            exit_button_width,
            exit_button_height,
            "X",
            self
        )

    def reset_game(self):
        self.snake = [(self.width//2 - (self.width//2 % 20), self.height//2 - (self.height//2 % 20))]
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
            while True:
                x = random.randrange(20, self.width - 40, 20)
                y = random.randrange(20, self.height - 40, 20)
                pos = (x - (x % 20), y - (y % 20))
                if pos not in self.obstacles and pos not in self.snake:
                    self.obstacles.append(pos)
                    break

    def generate_eggs(self):
        self.egg_positions = []
        self.egg_types = {}  # Dictionary to store egg types (normal or golden)
        for _ in range(5):
            while True:
                x = random.randrange(20, self.width - 40, 20)
                y = random.randrange(20, self.height - 40, 20)
                pos = (x - (x % 20), y - (y % 20))
                if pos not in self.obstacles and pos not in self.snake and pos not in self.egg_positions:
                    self.egg_positions.append(pos)
                    # Determine if this egg is golden
                    if random.random() < (0.05 * self.upgrades["golden_egg_chance"]):
                        self.egg_types[pos] = "golden"
                    else:
                        self.egg_types[pos] = "normal"
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
                
                if self.game_state == GameState.PLAYING and not self.showing_death_summary:
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
                    self.exit_button.handle_event(event)
                elif self.game_state == GameState.PAUSE:
                    for button in self.pause_buttons.values():
                        button.handle_event(event)
                elif self.game_state == GameState.SETTINGS:
                    self.settings.handle_input(event)
                elif self.game_state == GameState.GAMBLING:
                    self.gambling.handle_input(event)
                elif self.game_state == GameState.PLAYING and self.showing_death_summary:
                    self.death_menu_button.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == GameState.MENU:
                    if self.debug_button.handle_event(event):
                        self.debug_mode = not self.debug_mode
                        return
                    if self.exit_button.handle_event(event):
                        self.save_data()
                        pygame.quit()
                        sys.exit()
                    
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
                elif self.game_state == GameState.PLAYING and self.showing_death_summary:
                    if self.death_menu_button.handle_event(event):
                        self.showing_death_summary = False
                        self.reset_game()
                        self.start_transition(GameState.MENU)

    def load_assets(self):
        self.assets = {
            "wall": pygame.image.load("assets/wall_block.png").convert_alpha(),
            "spikes": pygame.image.load("assets/spikes.png").convert_alpha(),
            "egg": pygame.image.load("assets/egg.png").convert_alpha(),
            "golden_egg": pygame.image.load("assets/golden_egg.png").convert_alpha(),
            "snake": {
                "head": {
                    "up": pygame.image.load("assets/snake_head_up.png").convert_alpha(),
                    "down": pygame.image.load("assets/snake_head_down.png").convert_alpha(),
                    "left": pygame.image.load("assets/snake_head_left.png").convert_alpha(),
                    "right": pygame.image.load("assets/snake_head_right.png").convert_alpha()
                },
                "body": pygame.image.load("assets/snake_body.png").convert_alpha(),
                "tail": {
                    "up": pygame.image.load("assets/snake_head_up.png").convert_alpha(),
                    "down": pygame.image.load("assets/snake_head_down.png").convert_alpha(),
                    "left": pygame.image.load("assets/snake_head_left.png").convert_alpha(),
                    "right": pygame.image.load("assets/snake_head_right.png").convert_alpha()
                }
            }
        }

    def draw(self):
        self.screen.fill((20, 20, 20))
        
        if self.game_state == GameState.MENU:
            title_font = pygame.font.Font(None, int(74 * min(self.scale_x, self.scale_y)))
            title_shadow = title_font.render("Snake Game", True, (0, 0, 0))
            title_text = title_font.render("Snake Game", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.display_width//2, int(200 * self.scale_y)))
            self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
            self.screen.blit(title_text, title_rect)
            
            for button in self.menu_buttons.values():
                button.draw(self.screen)
            
            self.debug_button.text = "Debug: ON" if self.debug_mode else "Debug: OFF"
            self.debug_button.draw(self.screen)
            self.exit_button.draw(self.screen)
        
        elif self.game_state == GameState.PLAYING:
            # play area calc
            play_area_x = (self.display_width - self.width) // 2
            play_area_y = (self.display_height - self.height) // 2
            
            # grid lines
            for x in range(0, self.width, 20):
                scaled_x = play_area_x + x
                pygame.draw.line(self.screen, (30, 30, 30), (scaled_x, play_area_y), (scaled_x, play_area_y + self.height))
            for y in range(0, self.height, 20):
                scaled_y = play_area_y + y
                pygame.draw.line(self.screen, (30, 30, 30), (play_area_x, scaled_y), (play_area_x + self.width, scaled_y))
            
            # walls
            wall_size = 20
            for x in range(0, self.width, 20):
                for y in range(0, self.height, 20):
                    if x == 0 or x == self.width - 20 or y == 0 or y == self.height - 20:
                        self.screen.blit(self.assets["wall"], (play_area_x + x, play_area_y + y))
            
            # snake
            for i, segment in enumerate(self.snake):
                if i == 0:  # Head
                    if self.direction == (0, -20):
                        head_img = self.assets["snake"]["head"]["up"]
                    elif self.direction == (0, 20):
                        head_img = self.assets["snake"]["head"]["down"]
                    elif self.direction == (-20, 0):
                        head_img = self.assets["snake"]["head"]["left"]
                    else:
                        head_img = self.assets["snake"]["head"]["right"]
                    self.screen.blit(head_img, (play_area_x + segment[0], play_area_y + segment[1]))
                else:  # Body and Tail
                    self.screen.blit(self.assets["snake"]["body"], (play_area_x + segment[0], play_area_y + segment[1]))
            
            # eggs
            for egg in self.egg_positions:
                if self.egg_types.get(egg) == "golden":
                    self.screen.blit(self.assets["golden_egg"], (play_area_x + egg[0], play_area_y + egg[1]))
                else:
                    self.screen.blit(self.assets["egg"], (play_area_x + egg[0], play_area_y + egg[1]))
            
            # obstacles
            for obstacle in self.obstacles:
                self.screen.blit(self.assets["spikes"], (play_area_x + obstacle[0], play_area_y + obstacle[1]))
            
            # moving blocks
            for block in self.moving_blocks:
                self.screen.blit(self.assets["spikes"], (play_area_x + block['pos'][0], play_area_y + block['pos'][1]))
            
            # UI
            font = pygame.font.Font(None, int(36 * min(self.scale_x, self.scale_y)))
            
            length_text = font.render(f"Length: {len(self.snake)}", True, (255, 255, 255))
            score_text = font.render(f"Score: {self.total_eggs_collected}", True, (255, 255, 255))
            
            panel_width = max(length_text.get_width(), score_text.get_width()) + int(40 * self.scale_x)
            panel_height = int(80 * self.scale_y)
            
            panel_rect = pygame.Rect(int(10 * self.scale_x), int(10 * self.scale_y), panel_width, panel_height)
            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            pygame.draw.rect(panel_surface, (30, 30, 30, 180), panel_surface.get_rect(), border_radius=int(10 * min(self.scale_x, self.scale_y)))
            pygame.draw.rect(panel_surface, (60, 60, 60, 180), panel_surface.get_rect(), int(2 * min(self.scale_x, self.scale_y)), border_radius=int(10 * min(self.scale_x, self.scale_y)))
            self.screen.blit(panel_surface, panel_rect)
            
            length_shadow = font.render(f"Length: {len(self.snake)}", True, (0, 0, 0))
            score_shadow = font.render(f"Score: {self.total_eggs_collected}", True, (0, 0, 0))
            
            text_x = int(20 * self.scale_x)
            self.screen.blit(length_shadow, (text_x + 2, int(22 * self.scale_y)))
            self.screen.blit(score_shadow, (text_x + 2, int(57 * self.scale_y)))
            
            self.screen.blit(length_text, (text_x, int(20 * self.scale_y)))
            self.screen.blit(score_text, (text_x, int(55 * self.scale_y)))

            if self.debug_mode:
                debug_font = pygame.font.Font(None, int(24 * min(self.scale_x, self.scale_y)))
                magnet_range = 20 * self.upgrades["egg_magnet"] if self.upgrades["egg_magnet"] != 0 else 0
                golden_chance = 5 * self.upgrades["golden_egg_chance"]
                debug_text = debug_font.render(f"Magnet Range: {magnet_range}px | Golden Chance: {golden_chance}%", True, (255, 255, 255))
                debug_rect = debug_text.get_rect(topright=(self.display_width - int(20 * self.scale_x), int(20 * self.scale_y)))
                self.screen.blit(debug_text, debug_rect)

            if self.showing_death_summary:
                current_time = pygame.time.get_ticks()
                if current_time - self.death_summary_time < 4000:
                    summary_width = int(400 * self.scale_x)
                    summary_height = int(300 * self.scale_y)
                    summary_x = (self.display_width - summary_width) // 2
                    summary_y = (self.display_height - summary_height) // 2

                    summary_surface = pygame.Surface((summary_width, summary_height), pygame.SRCALPHA)
                    pygame.draw.rect(summary_surface, (30, 30, 30, 230), summary_surface.get_rect(), border_radius=int(15 * min(self.scale_x, self.scale_y)))
                    pygame.draw.rect(summary_surface, (60, 60, 60, 230), summary_surface.get_rect(), int(2 * min(self.scale_x, self.scale_y)), border_radius=int(15 * min(self.scale_x, self.scale_y)))
                    self.screen.blit(summary_surface, (summary_x, summary_y))

                    title_font = pygame.font.Font(None, int(48 * min(self.scale_x, self.scale_y)))
                    title_text = title_font.render("Game Over!", True, (255, 255, 255))
                    title_rect = title_text.get_rect(center=(summary_x + summary_width//2, summary_y + int(50 * self.scale_y)))
                    self.screen.blit(title_text, title_rect)

                    stats_font = pygame.font.Font(None, int(36 * min(self.scale_x, self.scale_y)))
                    stats = [
                        f"Length: {len(self.snake)}",
                        f"Score: {self.total_eggs_collected}",
                        f"Eggs Collected: {self.total_eggs_collected}"
                    ]

                    for i, stat in enumerate(stats):
                        stat_text = stats_font.render(stat, True, (255, 255, 255))
                        stat_rect = stat_text.get_rect(center=(summary_x + summary_width//2, summary_y + int(120 + i * 40) * self.scale_y))
                        self.screen.blit(stat_text, stat_rect)

                    self.death_menu_button.draw(self.screen)
                else:
                    self.showing_death_summary = False
                    self.reset_game()
                    self.start_transition(GameState.MENU)
        
        elif self.game_state == GameState.PAUSE:

            overlay = pygame.Surface((self.display_width, self.display_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            title_font = pygame.font.Font(None, int(74 * min(self.scale_x, self.scale_y)))
            title_shadow = title_font.render("Paused", True, (0, 0, 0))
            title_text = title_font.render("Paused", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.display_width//2, int(200 * self.scale_y)))
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
        
        self.update_transition()
        
        if self.game_state == GameState.PLAYING:
            if current_time - self.last_moving_block_time >= self.moving_block_interval:
                self.last_moving_block_time = current_time
                self.moving_block_interval = random.randint(1500, 3000)
                
                side = random.choice(['top', 'right', 'bottom', 'left'])
                if side == 'top':
                    x = random.randrange(20, self.width - 40, 20)
                    y = 20
                    direction = (0, 20)
                elif side == 'right':
                    x = self.width - 40
                    y = random.randrange(20, self.height - 40, 20)
                    direction = (-20, 0)
                elif side == 'bottom':
                    x = random.randrange(20, self.width - 40, 20)
                    y = self.height - 40
                    direction = (0, -20)
                else:  # left
                    x = 20
                    y = random.randrange(20, self.height - 40, 20)
                    direction = (20, 0)
                
                pos = (x - (x % 20), y - (y % 20))
                self.moving_blocks.append({
                    'pos': pos,
                    'direction': direction,
                    'last_move': current_time,
                    'move_interval': 1000
                })
            
            for block in self.moving_blocks[:]:
                if current_time - block['last_move'] >= block['move_interval']:
                    block['last_move'] = current_time
                    new_x = block['pos'][0] + block['direction'][0]
                    new_y = block['pos'][1] + block['direction'][1]
                    new_pos = (new_x - (new_x % 20), new_y - (new_y % 20))
                    
                    if (new_x < 20 or new_x >= self.width - 20 or 
                        new_y < 20 or new_y >= self.height - 20):
                        self.moving_blocks.remove(block)
                        continue
                    
                    block['pos'] = new_pos
            
            if current_time - self.last_move_time >= self.move_interval:
                self.last_move_time = current_time
                
                if self.direction_queue:
                    self.direction = self.direction_queue.pop(0)

                new_x = self.snake[0][0] + self.direction[0]
                new_y = self.snake[0][1] + self.direction[1]
                new_head = (new_x - (new_x % 20), new_y - (new_y % 20))
                
                for block in self.moving_blocks:
                    if new_head == block['pos']:
                        self.showing_death_summary = True
                        self.death_summary_time = current_time
                        return
                
                if (new_x < 20 or new_x >= self.width - 20 or
                    new_y < 20 or new_y >= self.height - 20 or
                    new_head in self.snake or new_head in self.obstacles):
                    self.showing_death_summary = True
                    self.death_summary_time = current_time
                    return

                self.snake.insert(0, new_head)
                
                if self.upgrades["egg_magnet"] != 0:
                    magnet_range = 20 * self.upgrades["egg_magnet"]
                    for egg in self.egg_positions[:]:
                        dx = egg[0] - new_head[0]
                        dy = egg[1] - new_head[1]
                        distance = (dx * dx + dy * dy) ** 0.5
                        if distance <= magnet_range:
                            egg_type = self.egg_types.pop(egg)
                            self.egg_positions.remove(egg)
                            if egg_type == "golden":
                                self.eggs += 10 * self.upgrades["currency_multiplier"]
                                self.eggs_collected += 10
                                self.total_eggs_collected += 10 * self.upgrades["currency_multiplier"]
                            else:
                                self.eggs += self.upgrades["currency_multiplier"]
                                self.eggs_collected += 1
                                self.total_eggs_collected += self.upgrades["currency_multiplier"]
                
                if new_head in self.egg_positions:
                    # Collect the egg at the head position
                    egg_type = self.egg_types.pop(new_head)
                    self.egg_positions.remove(new_head)
                    if egg_type == "golden":
                        self.eggs += 10 * self.upgrades["currency_multiplier"]
                        self.eggs_collected += 10
                        self.total_eggs_collected += 10 * self.upgrades["currency_multiplier"]
                    else:
                        self.eggs += self.upgrades["currency_multiplier"]
                        self.eggs_collected += 1
                        self.total_eggs_collected += self.upgrades["currency_multiplier"]
                
                if len(self.egg_positions) == 0:
                    self.generate_eggs()
                if self.eggs_collected >= self.upgrades["grow_rate"]:
                    self.eggs_collected = 0
                else:
                    self.snake.pop()
        elif self.game_state == GameState.GAMBLING:
            self.gambling.update()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 