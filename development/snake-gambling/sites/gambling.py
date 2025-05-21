import pygame
import random
import math
from sites.button import Button

class Gambling:
    def __init__(self, game):
        self.game = game
        self.current_game = None
        self.bet_amount = 10
        self.slots = ["lemon", "cherry", "orange", "banana", "grape", "strawberry", "melon"]
        self.slot_multipliers = {
            "lemon": 1.25,
            "cherry": 1.5,
            "orange": 2.0,
            "banana": 2.5,
            "grape": 3.0,
            "strawberry": 5.0,
            "melon": 7.5
        }
        self.slot_results = ["lemon", "lemon", "lemon"]
        self.spinning = False
        self.spin_time = 0
        self.slot_spin_times = [0, 0, 0]
        self.slot_spin_delays = [0, 500, 1000]
        self.slot_spin_speeds = [0, 0, 0]
        self.max_spin_speed = 100
        self.acceleration = 200
        self.deceleration = 150
        self.wheel_angle = 0
        self.wheel_spinning = False
        self.last_frame_time = pygame.time.get_ticks()
        self.rotation_count = 0
        self.start_angle = 0
        self.total_rotation = 0
        self.initial_phase = True
        self.last_win = None
        self.last_multiplier = None
        self.win_display_time = 0
        self.non_matching_spins = 0
        self.max_non_matching_spins = 5
        
        self.slot_positions = [
            (34, 142), 
            (86, 142), 
            (138, 142) 
        ]
        self.slot_size = (50, 50)
        
        self.load_slot_assets()
        
        # wheel angles
        self.wheel_sections = [
            {"name": "1 POINT", "multiplier": 0.5, "odds": 0.48, "ranges": [
                (350, 3), (18, 31), (46, 59), (74, 88), (103, 117), (147, 160),
                (175, 189), (204, 219), (234, 248), (264, 278), (293, 308), (322, 336)
            ]},
            {"name": "3 POINT", "multiplier": 1.25, "odds": 0.24, "ranges": [
                (4, 17), (60, 73), (132, 146), (190, 203), (249, 263), (309, 321)
            ]},
            {"name": "5 POINT", "multiplier": 2.0, "odds": 0.16, "ranges": [
                (89, 102), (118, 131), (220, 233), (337, 349)
            ]},
            {"name": "10 POINT", "multiplier": 5.0, "odds": 0.08, "ranges": [
                (32, 45), (161, 174)
            ]},
            {"name": "20 POINT", "multiplier": 10.0, "odds": 0.04, "ranges": [
                (279, 292)
            ]}
        ]
        
        self.setup_buttons()
        self.load_wheel_image()

    def get_current_section(self):
        angle = self.wheel_angle % 360
        for section in self.wheel_sections:
            for start, end in section["ranges"]:
                if start <= end:
                    if start <= angle <= end:
                        return section
                else:  
                    if angle >= start or angle <= end:
                        return section
        return None

    def load_wheel_image(self):
        try:
            self.wheel_image = pygame.image.load("assets/wheel.png")
            self.wheel_image = pygame.transform.scale(self.wheel_image, (400, 400))
            self.wheel_rect = self.wheel_image.get_rect()
        except:
            print("Warning: wheel.png not found. Using default wheel.")
            self.wheel_image = None

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.game.width // 2 - button_width // 2  
        
        self.mode_buttons = {
            "slots": Button(center_x, 300, button_width, button_height, "Slots", self.game),
            "wheel": Button(center_x, 370, button_width, button_height, "Wheel", self.game)
        }
        
        bottom_y = self.game.height - 150  
        center_x = self.game.width // 2  
        button_spacing = 200  
        self.bet_buttons = {
            "increase": Button(center_x - button_spacing, bottom_y - 60, button_width//2, button_height, "+", self.game),  
            "decrease": Button(center_x + button_spacing - button_width//2, bottom_y - 60, button_width//2, button_height, "-", self.game)   
        }
        
        self.spin_button = Button(center_x - button_width//2, bottom_y, button_width, button_height, "Spin", self.game)
        
        debug_button_width = 60
        debug_button_height = 30
        debug_start_x = 10
        debug_start_y = 190  
        self.debug_buttons = {
            "fine_minus": Button(debug_start_x, debug_start_y, debug_button_width, debug_button_height, "-1°", self.game),
            "fine_plus": Button(debug_start_x + 70, debug_start_y, debug_button_width, debug_button_height, "+1°", self.game)
        }

    def get_random_section(self):
        
        rand = random.random()
        cumulative_prob = 0
        
       
        for section in self.wheel_sections:
            cumulative_prob += section["odds"]
            if rand <= cumulative_prob:
                return section
        
        
        return self.wheel_sections[0]

    def get_random_angle_for_section(self, section):
        
        start, end = random.choice(section["ranges"])
        
       
        if start > end:
            
            if random.random() < 0.5:
                return random.uniform(start, 360)
            else:
                return random.uniform(0, end)
        else:
            
            return random.uniform(start, end)

    def draw(self, screen):
        screen.fill((20, 20, 20))
        
        font = pygame.font.Font(None, int(74 * min(self.game.scale_x, self.game.scale_y)))
        title_shadow = font.render("Gambling", True, (0, 0, 0))
        title_text = font.render("Gambling", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.display_width//2, int(50 * self.game.scale_y)))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        eggs_text = font.render(f"{self.game.eggs}", True, (255, 255, 255))
        eggs_shadow = font.render(f"{self.game.eggs}", True, (0, 0, 0))
        egg_img = pygame.image.load("assets/egg.png").convert_alpha()
        egg_img = pygame.transform.scale(egg_img, (int(30 * self.game.scale_x), int(30 * self.game.scale_y)))
        screen.blit(egg_img, (int(10 * self.game.scale_x), int(10 * self.game.scale_y)))
        screen.blit(eggs_shadow, (int(45 * self.game.scale_x), int(12 * self.game.scale_y)))
        screen.blit(eggs_text, (int(43 * self.game.scale_x), int(10 * self.game.scale_y)))
        
        if self.current_game is None:
            subtitle = font.render("Select Game Mode", True, (255, 255, 255))
            screen.blit(subtitle, (self.game.display_width//2 - subtitle.get_width()//2, int(200 * self.game.scale_y)))
            
            for button in self.mode_buttons.values():
                button.draw(screen)
        else:
            
            bet_shadow = font.render(f"Bet: {self.bet_amount}", True, (0, 0, 0))
            bet_text = font.render(f"Bet: {self.bet_amount}", True, (255, 255, 255))
            bet_rect = bet_text.get_rect(center=(self.game.display_width//2, int(350 * self.game.scale_y)))
            screen.blit(bet_shadow, (bet_rect.x + 2, bet_rect.y + 2))
            screen.blit(bet_text, bet_rect)
            
            
            for button in self.bet_buttons.values():
                button.draw(screen)
            self.spin_button.draw(screen)
            
            if self.current_game == "slots":
                self.draw_slots(screen)
                
                for button in self.bet_buttons.values():
                    button.draw(screen)
                if not self.spinning and self.bet_amount > 0:
                    self.spin_button.draw(screen)
            else:
                self.draw_wheel(screen)
                
                for button in self.bet_buttons.values():
                    button.draw(screen)
                if not self.wheel_spinning and self.bet_amount > 0:
                    self.spin_button.draw(screen)
                
                
                if self.game.debug_mode:
                    debug_text = font.render(f"Wheel Angle: {self.wheel_angle:.1f}°", True, (255, 255, 255))
                    screen.blit(debug_text, (int(10 * self.game.scale_x), int(80 * self.game.scale_y)))
                    
                    current_section = self.get_current_section()
                    if current_section:
                        section_text = font.render(
                            f"Current Section: {current_section['name']} ({current_section['multiplier']}x)", 
                            True, (255, 255, 255)
                        )
                        screen.blit(section_text, (int(10 * self.game.scale_x), int(120 * self.game.scale_y)))
                    
                    
                    if self.wheel_spinning:
                        rotation_text = font.render(f"Rotations: {self.rotation_count}", True, (255, 255, 255))
                        screen.blit(rotation_text, (int(10 * self.game.scale_x), int(160 * self.game.scale_y)))
                    
                    
                    for button in self.debug_buttons.values():
                        button.draw(screen)

        back_text = font.render("Press ESC to return", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(self.game.display_width//2, self.game.display_height - int(50 * self.game.scale_y)))
        back_shadow = font.render("Press ESC to return", True, (0, 0, 0))
        screen.blit(back_shadow, (back_rect.x + 2, back_rect.y + 2))
        screen.blit(back_text, back_rect)

    def draw_slots(self, screen):
        if not self.slot_machine:
            return

        if self.last_win is not None and pygame.time.get_ticks() - self.win_display_time < 2000:
            font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
            win_text = font.render(f"Win: {self.last_win} eggs!", True, (255, 215, 0))
            screen.blit(win_text, (self.game.display_width//2 - win_text.get_width()//2, int(200 * self.game.scale_y)))

        slot_machine_rect = self.slot_machine.get_rect(center=(self.game.display_width//2, self.game.display_height//2))
        screen.blit(self.slot_machine, slot_machine_rect)

        for i, fruit in enumerate(self.slot_results):
            if fruit in self.fruit_images:
                fruit_img = self.fruit_images[fruit]
                slot_x = slot_machine_rect.x + self.slot_positions[i][0]
                slot_y = slot_machine_rect.y + self.slot_positions[i][1]
                screen.blit(fruit_img, (slot_x, slot_y))

        font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        bet_shadow = font.render(f"Bet: {self.bet_amount}", True, (0, 0, 0))
        bet_text = font.render(f"Bet: {self.bet_amount}", True, (255, 255, 255))
        bottom_y = self.game.height - 150
        bet_rect = bet_text.get_rect(center=(self.game.display_width//2, bottom_y + 230))
        screen.blit(bet_shadow, (bet_rect.x + 2, bet_rect.y + 2))
        screen.blit(bet_text, bet_rect)

    def draw_wheel(self, screen):
        center_x = self.game.display_width//2
        center_y = self.game.display_height//2 - int(50 * self.game.scale_y)

        if self.wheel_image:
            wheel_size = int(400 * min(self.game.scale_x, self.game.scale_y))
            scaled_wheel = pygame.transform.scale(self.wheel_image, (wheel_size, wheel_size))
            rotated_wheel = pygame.transform.rotate(scaled_wheel, self.wheel_angle)
            wheel_rect = rotated_wheel.get_rect(center=(center_x, center_y))
            screen.blit(rotated_wheel, wheel_rect)
        else:
            radius = int(200 * min(self.game.scale_x, self.game.scale_y))
            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), radius + 5)
        
        pointer_points = [
            (center_x - int(10 * self.game.scale_x), center_y - int(210 * self.game.scale_y)),
            (center_x + int(10 * self.game.scale_x), center_y - int(210 * self.game.scale_y)),
            (center_x, center_y - int(190 * self.game.scale_y))
        ]
        pygame.draw.polygon(screen, (255, 255, 255), pointer_points)

        bet_font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        bet_shadow = bet_font.render(f"Bet: {self.bet_amount}", True, (0, 0, 0))
        bet_text = bet_font.render(f"Bet: {self.bet_amount}", True, (255, 255, 255))
        bottom_y = self.game.height - 150
        bet_rect = bet_text.get_rect(center=(center_x, bottom_y + 230))
        screen.blit(bet_shadow, (bet_rect.x + 2, bet_rect.y + 2))
        screen.blit(bet_text, bet_rect)

        current_time = pygame.time.get_ticks()
        if self.last_win and current_time - self.win_display_time < 3000:
            win_font = pygame.font.Font(None, int(48 * min(self.game.scale_x, self.game.scale_y)))
            win_text = f"Won: {self.last_win} eggs! (x{self.last_multiplier})"
            win_shadow = win_font.render(win_text, True, (0, 0, 0))
            win_text = win_font.render(win_text, True, (255, 215, 0))
            win_rect = win_text.get_rect(center=(self.game.display_width//2, self.game.display_height//2))
            screen.blit(win_shadow, (win_rect.x + 2, win_rect.y + 2))
            screen.blit(win_text, win_rect)

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_frame_time) / 1000.0  
        self.last_frame_time = current_time

        if self.spinning:
            all_slots_stopped = True
            for i in range(3):
                if current_time - self.spin_time >= self.slot_spin_delays[i]:
                    slot_spin_time = current_time - (self.spin_time + self.slot_spin_delays[i])
                    
                    if slot_spin_time < 2000:
                        all_slots_stopped = False
                        
                        if slot_spin_time < 500:
                            self.slot_spin_speeds[i] = min(self.slot_spin_speeds[i] + self.acceleration * delta_time, self.max_spin_speed)
                        elif slot_spin_time > 1500:
                            self.slot_spin_speeds[i] = max(self.slot_spin_speeds[i] - self.deceleration * delta_time, 0)
                        
                        if self.slot_spin_speeds[i] > 0 and current_time % int(1000 / self.slot_spin_speeds[i]) < int(500 / self.slot_spin_speeds[i]):
                            self.slot_results[i] = self.get_weighted_random_fruit(i)
                    else:
                        self.slot_spin_speeds[i] = 0
                        if self.slot_results[i] == self.slot_results[0] and i > 0:
                            self.slot_results[i] = random.choice([f for f in self.slots if f != self.slot_results[0]])

            if all_slots_stopped:
                self.spinning = False
                self.check_slots_win()

        if self.wheel_spinning:
            
            if not hasattr(self, 'target_angle'):
                target_section = self.get_random_section()
                self.target_angle = self.get_random_angle_for_section(target_section)
                self.start_angle = self.wheel_angle
                self.rotation_count = 0
                self.total_rotation = 0
                self.spin_start_time = current_time
                
                
                angle_diff_from_start = (self.target_angle - self.start_angle) % 360
                self.target_is_close = angle_diff_from_start <= 120
                print(f"Target section: {target_section['name']} ({target_section['multiplier']}x)")
                print(f"Target angle: {self.target_angle:.1f}°")
                print(f"Start angle: {self.start_angle:.1f}°")
                print(f"Angle diff from start: {angle_diff_from_start:.1f}°")
                print(f"Target is within 120°: {self.target_is_close}")
            

            current_angle = self.wheel_angle % 360
            target_angle = self.target_angle % 360
            

            rotation_this_frame = 360 * delta_time
            self.total_rotation += rotation_this_frame
            self.rotation_count = int(self.total_rotation / 360)  
            
            
            should_ease = False
            
            if self.target_is_close:
               
                if self.rotation_count >= 2:
                    
                    angle_diff_to_target = (target_angle - current_angle) % 360
                    should_ease = angle_diff_to_target <= 120
            else:
                
                if self.rotation_count >= 3:
                    
                    angle_diff_to_target = (target_angle - current_angle) % 360
                    should_ease = angle_diff_to_target <= 120
            
            if should_ease:
                angle_diff_to_target = (target_angle - current_angle) % 360
                
                if angle_diff_to_target < 0.1 or angle_diff_to_target > 359.9:
                    self.wheel_angle = self.target_angle
                    self.wheel_spinning = False
                    delattr(self, 'target_angle')
                    delattr(self, 'spin_start_time')
                    self.check_wheel_win()
                    return
                
                ease_progress = 1 - (angle_diff_to_target / 120)
                ease_progress = 1 - (1 - ease_progress) ** 3
                
                target_speed = 360 * (1 - ease_progress)
                target_speed = max(target_speed, 30)
                rotation_this_frame = target_speed * delta_time
                
                if rotation_this_frame > angle_diff_to_target:
                    rotation_this_frame = angle_diff_to_target
                
                self.wheel_angle = (self.wheel_angle + rotation_this_frame) % 360
                self.total_rotation += rotation_this_frame
            else:
                self.wheel_angle = (self.wheel_angle + rotation_this_frame) % 360

    def get_weighted_random_fruit(self, index):
        if self.spinning:
            available_fruits = [f for f in self.slots if f != self.slot_results[index]]
            if self.non_matching_spins > 0:
                if index == 0:
                    return random.choice(available_fruits)
                elif index == 1:
                    if random.random() < min(0.2 * self.non_matching_spins, 0.8):
                        return self.slot_results[0]
                    return random.choice(available_fruits)
                else:
                    if random.random() < min(0.15 * self.non_matching_spins, 0.6):
                        return self.slot_results[0]
                    return random.choice(available_fruits)
            return random.choice(available_fruits)
        return random.choice(self.slots)

    def check_slots_win(self):
        if len(set(self.slot_results)) == 1:
            fruit = self.slot_results[0]
            multiplier = self.slot_multipliers[fruit] * 3
            self.non_matching_spins = 0
        elif len(set(self.slot_results)) == 2:
            for fruit in set(self.slot_results):
                if self.slot_results.count(fruit) == 2:
                    multiplier = self.slot_multipliers[fruit] * 1
                    self.non_matching_spins = 0
                    break
        else:
            multiplier = 0.5
            self.non_matching_spins = min(self.non_matching_spins + 1, self.max_non_matching_spins)

        win_amount = int(self.bet_amount * multiplier)
        self.game.eggs += win_amount
        self.last_win = win_amount
        self.last_multiplier = multiplier
        self.win_display_time = pygame.time.get_ticks()

    def check_wheel_win(self):
        current_section = self.get_current_section()
        if current_section:
            winnings = int(self.bet_amount * current_section["multiplier"]) 
            self.game.eggs += winnings
            self.last_win = winnings
            self.last_multiplier = current_section["multiplier"]
            self.win_display_time = pygame.time.get_ticks()
            print(f"Won {winnings} eggs! ({current_section['name']} - {current_section['multiplier']}x)")

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.current_game is None:
                for button in self.mode_buttons.values():
                    button.handle_event(event)
            else:
                for button in self.bet_buttons.values():
                    button.handle_event(event)
                self.spin_button.handle_event(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_game is None:
                for button_name, button in self.mode_buttons.items():
                    if button.handle_event(event):
                        self.current_game = button_name
                        return
            else:
                for button_name, button in self.bet_buttons.items():
                    if button.handle_event(event):
                        if button_name == "increase":
                            self.bet_amount = min(self.bet_amount + 10, self.game.eggs)
                        else:
                            self.bet_amount = max(self.bet_amount - 10, 10)
                        return
                
                if not self.spinning and not self.wheel_spinning:
                    if self.spin_button.handle_event(event):
                        if self.game.eggs >= self.bet_amount:
                            self.game.eggs -= self.bet_amount
                            if self.current_game == "slots":
                                self.spinning = True
                                self.spin_time = pygame.time.get_ticks()
                            else:
                                self.wheel_spinning = True
                                if hasattr(self, 'target_angle'):
                                    delattr(self, 'target_angle')
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.wheel_spinning:
                self.wheel_spinning = False
                if hasattr(self, 'target_angle'):
                    self.wheel_angle = self.target_angle
                    self.check_wheel_win()
                    delattr(self, 'target_angle')
                self.game.game_state = GameState.MENU
                self.current_game = None 

    def load_slot_assets(self):
        try:
            self.slot_machine = pygame.image.load("assets/slots_machine.png").convert_alpha()
            self.fruit_images = {
                "lemon": pygame.image.load("assets/slots_lemon.png").convert_alpha(),
                "cherry": pygame.image.load("assets/slots_cherry.png").convert_alpha(),
                "orange": pygame.image.load("assets/slots_orange.png").convert_alpha(),
                "banana": pygame.image.load("assets/slots_banana.png").convert_alpha(),
                "grape": pygame.image.load("assets/slots_grape.png").convert_alpha(),
                "strawberry": pygame.image.load("assets/slots_strawberry.png").convert_alpha(),
                "melon": pygame.image.load("assets/slots_watermelon.png").convert_alpha()
            }
        except Exception as e:
            print(f"Error loading slot assets: {e}")
            self.slot_machine = None
            self.fruit_images = {}
