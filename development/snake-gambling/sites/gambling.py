import pygame
import random
import math
from sites.button import Button

class Gambling:
    def __init__(self, game):
        self.game = game
        self.current_game = None
        self.bet_amount = 10
        self.slots = ["🍎", "🍋", "🍇", "🍒", "7️⃣", "💎"]
        self.slot_results = ["🍎", "🍎", "🍎"]
        self.spinning = False
        self.spin_time = 0
        self.wheel_angle = 0
        self.wheel_spinning = False
        self.last_frame_time = pygame.time.get_ticks()
        self.rotation_count = 0
        self.start_angle = 0
        self.total_rotation = 0
        self.initial_phase = True
        
        # Winkel definitionen
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
        
        # Mode selection buttons
        self.mode_buttons = {
            "slots": Button(center_x, 300, button_width, button_height, "Slots"),
            "wheel": Button(center_x, 370, button_width, button_height, "Wheel")
        }
        
        
        bottom_y = self.game.height - 150  
        center_x = self.game.width // 2  
        self.bet_buttons = {
            "increase": Button(center_x - 110 - 20, bottom_y - 60, button_width//2, button_height, "+"),  
            "decrease": Button(center_x + 10 + 20, bottom_y - 60, button_width//2, button_height, "-")   
        }
        
        self.spin_button = Button(center_x - button_width//2, bottom_y, button_width, button_height, "Spin")

        
        debug_button_width = 60
        debug_button_height = 30
        debug_start_x = 10
        debug_start_y = 190  
        self.debug_buttons = {
            "fine_minus": Button(debug_start_x, debug_start_y, debug_button_width, debug_button_height, "-1°"),
            "fine_plus": Button(debug_start_x + 70, debug_start_y, debug_button_width, debug_button_height, "+1°")
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
        
        # Draw title with shadow
        font = pygame.font.Font(None, 74)
        title_shadow = font.render("Gambling", True, (0, 0, 0))
        title_text = font.render("Gambling", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width//2, 50))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title_text, title_rect)
        
        # Draw eggs count with shadow
        font = pygame.font.Font(None, 36)
        eggs_shadow = font.render(f"Eggs: {self.game.eggs}", True, (0, 0, 0))
        eggs_text = font.render(f"Eggs: {self.game.eggs}", True, (255, 255, 255))
        screen.blit(eggs_shadow, (12, 12))
        screen.blit(eggs_text, (10, 10))
        
        if self.current_game is None:
            
            subtitle = font.render("Select Game Mode", True, (255, 255, 255))
            screen.blit(subtitle, (self.game.width//2 - subtitle.get_width()//2, 200))
            
            for button in self.mode_buttons.values():
                button.draw(screen)
        else:
            # Draw bet amount with shadow
            bet_shadow = font.render(f"Bet: {self.bet_amount}", True, (0, 0, 0))
            bet_text = font.render(f"Bet: {self.bet_amount}", True, (255, 255, 255))
            bet_rect = bet_text.get_rect(center=(self.game.width//2, 350))
            screen.blit(bet_shadow, (bet_rect.x + 2, bet_rect.y + 2))
            screen.blit(bet_text, bet_rect)
            
            # Draw bet buttons and spin button
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
                
                # Draw debug info
                debug_text = font.render(f"Wheel Angle: {self.wheel_angle:.1f}°", True, (255, 255, 255))
                screen.blit(debug_text, (10, 80))
                
                current_section = self.get_current_section()
                if current_section:
                    section_text = font.render(
                        f"Current Section: {current_section['name']} ({current_section['multiplier']}x)", 
                        True, (255, 255, 255)
                    )
                    screen.blit(section_text, (10, 120))
                
                # Draw rotation counter
                if self.wheel_spinning:
                    rotation_text = font.render(f"Rotations: {self.rotation_count}", True, (255, 255, 255))
                    screen.blit(rotation_text, (10, 160))
                
                # Draw debug buttons
                for button in self.debug_buttons.values():
                    button.draw(screen)

        back_text = font.render("Press ESC to return", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(self.game.width//2, self.game.height - 50))
        screen.blit(back_shadow, (back_rect.x + 2, back_rect.y + 2))
        screen.blit(back_text, back_rect)

    def draw_slots(self, screen):
        font = pygame.font.Font(None, 100)
        slot_width = 150
        start_x = self.game.width//2 - (slot_width * 1.5)
        
        
        for i in range(3):
            pygame.draw.rect(screen, (100, 100, 100), (start_x + i * slot_width, 300, slot_width, slot_width), 2)
        
        
        for i, symbol in enumerate(self.slot_results):
            text = font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=(start_x + i * slot_width + slot_width//2, 300 + slot_width//2))
            screen.blit(text, text_rect)

        font = pygame.font.Font(None, 36)
        bet_text = font.render(f"Bet: {self.bet_amount} eggs", True, (255, 255, 255))
        screen.blit(bet_text, (self.game.width//2 - bet_text.get_width()//2, 400))

    def draw_wheel(self, screen):
        center_x = self.game.width//2
        center_y = self.game.height//2 - 50

        if self.wheel_image:
            # Draw wheel image
            rotated_wheel = pygame.transform.rotate(self.wheel_image, self.wheel_angle)
            wheel_rect = rotated_wheel.get_rect(center=(center_x, center_y))
            screen.blit(rotated_wheel, wheel_rect)
        else:
            
            radius = 200
            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), radius + 5)

        
        pointer_points = [
            (center_x - 10, center_y - 210),  
            (center_x + 10, center_y - 210),  
            (center_x, center_y - 190)        
        ]
        pygame.draw.polygon(screen, (255, 255, 255), pointer_points)

        font = pygame.font.Font(None, 36)
        bet_text = font.render(f"Bet: {self.bet_amount} eggs", True, (255, 255, 255))
        screen.blit(bet_text, (self.game.width//2 - bet_text.get_width()//2, center_y + 210))

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_frame_time) / 1000.0  
        self.last_frame_time = current_time

        if self.spinning:
            self.spin_time += 1
            if self.spin_time >= 30:
                self.spin_time = 0
                self.spinning = False
                self.check_slots_win()
            else:
                
                self.slot_results = [random.choice(self.slots) for _ in range(3)]

        if self.wheel_spinning:
            # Calculate target angle based on odds
            if not hasattr(self, 'target_angle'):
                target_section = self.get_random_section()
                self.target_angle = self.get_random_angle_for_section(target_section)
                self.start_angle = self.wheel_angle
                self.rotation_count = 0
                self.total_rotation = 0
                self.spin_start_time = current_time
                
                # Calculate if target is within 120 degrees of start position
                angle_diff_from_start = (self.target_angle - self.start_angle) % 360
                self.target_is_close = angle_diff_from_start <= 120
                print(f"Target section: {target_section['name']} ({target_section['multiplier']}x)")
                print(f"Target angle: {self.target_angle:.1f}°")
                print(f"Start angle: {self.start_angle:.1f}°")
                print(f"Angle diff from start: {angle_diff_from_start:.1f}°")
                print(f"Target is within 120°: {self.target_is_close}")
            
            # Calculate current angle and distance to target
            current_angle = self.wheel_angle % 360
            target_angle = self.target_angle % 360
            
            # Calculate rotations completed
            rotation_this_frame = 360 * delta_time
            self.total_rotation += rotation_this_frame
            self.rotation_count = int(self.total_rotation / 360)  
            
            
            should_ease = False
            
            if self.target_is_close:
               
                if self.rotation_count >= 2:
                    # Calculate distance from current position to target
                    angle_diff_to_target = (target_angle - current_angle) % 360
                    should_ease = angle_diff_to_target <= 120
            else:
                # If target is far from start, do 3 rotations first
                if self.rotation_count >= 3:
                    
                    angle_diff_to_target = (target_angle - current_angle) % 360
                    should_ease = angle_diff_to_target <= 120
            
            if should_ease:
                # Calculate how far we are into the easing (0 to 1)
                # 0 = 120 degrees away, 1 = at target
                angle_diff_to_target = (target_angle - current_angle) % 360
                
                # If we're very close to target, snap to it
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

    def check_slots_win(self):
        if len(set(self.slot_results)) == 1:
            multiplier = 5 if self.slot_results[0] == "💎" else 3
            self.game.eggs += self.bet_amount * multiplier

    def check_wheel_win(self):
        current_section = self.get_current_section()
        if current_section:
            winnings = int(self.bet_amount * current_section["multiplier"]) 
            self.game.eggs += winnings
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
                        if button_name == "wheel": 
                            self.current_game = button_name
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
                            self.wheel_spinning = True
                            if hasattr(self, 'target_angle'):
                                delattr(self, 'target_angle')
        
        # Handle escape key
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.wheel_spinning:
                # End spin immediately and pay out
                self.wheel_spinning = False
                if hasattr(self, 'target_angle'):
                    self.wheel_angle = self.target_angle
                    self.check_wheel_win()
                    delattr(self, 'target_angle')
                self.game.game_state = GameState.MENU
                self.current_game = None 
