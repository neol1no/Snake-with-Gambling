import pygame
import random
import math

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
        self.rotation_count = 0  # Track number of rotations
        self.start_angle = 0     # Store initial angle for rotation counting
        self.total_rotation = 0  # Track total rotation without modulo
        self.initial_phase = True # Track if we're in initial 3 rotations phase
        
        # Define wheel sections with their angle ranges and properties
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
                else:  # Handle ranges that cross 360/0
                    if angle >= start or angle <= end:
                        return section
        return None

    def load_wheel_image(self):
        try:
            self.wheel_image = pygame.image.load("wheel.png")
            self.wheel_image = pygame.transform.scale(self.wheel_image, (400, 400))
            self.wheel_rect = self.wheel_image.get_rect()
        except:
            print("Warning: wheel.png not found. Using default wheel.")
            self.wheel_image = None

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        mode_center_x = self.game.width // 2 - button_width // 2  # Original center calculation for mode buttons
        
        self.mode_buttons = {
            "slots": Button(mode_center_x, 300, button_width, button_height, "Slots"),
            "wheel": Button(mode_center_x, 370, button_width, button_height, "Wheel")
        }
        
        # Move bet buttons and spin button to bottom
        bottom_y = self.game.height - 150  # Position above "Press ESC to return"
        center_x = self.game.width // 2  # Exact center for bet buttons
        self.bet_buttons = {
            "increase": Button(center_x - 110 - 20, bottom_y - 60, button_width//2, button_height, "+"),  # 20px left of original position
            "decrease": Button(center_x + 10 + 20, bottom_y - 60, button_width//2, button_height, "-")   # 20px right of original position
        }
        
        self.spin_button = Button(center_x - button_width//2, bottom_y, button_width, button_height, "Spin")

        # Debug buttons for wheel
        debug_button_width = 60
        debug_button_height = 30
        debug_start_x = 10
        debug_start_y = 190  # Moved below the rotation counter (was 160)
        self.debug_buttons = {
            "fine_minus": Button(debug_start_x, debug_start_y, debug_button_width, debug_button_height, "-1°"),
            "fine_plus": Button(debug_start_x + 70, debug_start_y, debug_button_width, debug_button_height, "+1°")
        }

    def get_random_section(self):
        # Generate a random number between 0 and 1
        rand = random.random()
        cumulative_prob = 0
        
        # Find which section the random number falls into based on odds
        for section in self.wheel_sections:
            cumulative_prob += section["odds"]
            if rand <= cumulative_prob:
                return section
        
        # Fallback to first section (should never happen)
        return self.wheel_sections[0]

    def get_random_angle_for_section(self, section):
        # Pick a random range from the section
        start, end = random.choice(section["ranges"])
        
        # If the range crosses 360/0
        if start > end:
            # Generate angle between start and 360, or 0 and end
            if random.random() < 0.5:
                return random.uniform(start, 360)
            else:
                return random.uniform(0, end)
        else:
            # Generate angle between start and end
            return random.uniform(start, end)

    def draw(self, screen):
        screen.fill((20, 20, 20))
        font = pygame.font.Font(None, 74)
        title = font.render("Gambling", True, (255, 255, 255))
        screen.blit(title, (self.game.width//2 - title.get_width()//2, 50))

        font = pygame.font.Font(None, 36)
        eggs_text = font.render(f"Eggs: {self.game.eggs}", True, (255, 255, 255))
        screen.blit(eggs_text, (10, 10))

        if self.current_game is None:
            # Draw mode selection screen
            subtitle = font.render("Select Game Mode", True, (255, 255, 255))
            screen.blit(subtitle, (self.game.width//2 - subtitle.get_width()//2, 200))
            
            for button in self.mode_buttons.values():
                button.draw(screen)
        else:
            if self.current_game == "slots":
                self.draw_slots(screen)
                # Draw buttons below slots
                for button in self.bet_buttons.values():
                    button.draw(screen)
                if not self.spinning and self.bet_amount > 0:
                    self.spin_button.draw(screen)
            else:
                # Draw wheel first
                self.draw_wheel(screen)
                # Draw buttons on top
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
        screen.blit(back_text, (self.game.width//2 - back_text.get_width()//2, self.game.height - 50))

    def draw_slots(self, screen):
        font = pygame.font.Font(None, 100)
        slot_width = 150
        start_x = self.game.width//2 - (slot_width * 1.5)
        
        # Draw slot frames
        for i in range(3):
            pygame.draw.rect(screen, (100, 100, 100), (start_x + i * slot_width, 300, slot_width, slot_width), 2)
        
        # Draw symbols
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
            # Fallback to drawing wheel sections
            radius = 200
            pygame.draw.circle(screen, (50, 50, 50), (center_x, center_y), radius + 5)
            
            for section in self.wheel_sections:
                for start, end in section["ranges"]:
                    pygame.draw.arc(screen, section["color"], 
                                  (center_x - radius, center_y - radius, radius * 2, radius * 2),
                                  math.radians(start), math.radians(end), radius)

        # Draw pointer
        pointer_points = [
            (center_x - 10, center_y - 210),  # Left top point
            (center_x + 10, center_y - 210),  # Right top point
            (center_x, center_y - 190)        # Bottom point
        ]
        pygame.draw.polygon(screen, (255, 255, 255), pointer_points)

        font = pygame.font.Font(None, 36)
        bet_text = font.render(f"Bet: {self.bet_amount} eggs", True, (255, 255, 255))
        screen.blit(bet_text, (self.game.width//2 - bet_text.get_width()//2, center_y + 210))

    def update(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_frame_time) / 1000.0  # Convert to seconds
        self.last_frame_time = current_time

        if self.spinning:
            self.spin_time += 1
            if self.spin_time >= 30:
                self.spin_time = 0
                self.spinning = False
                self.check_slots_win()
            else:
                # Update slot symbols during spin
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
            self.rotation_count = int(self.total_rotation / 360)  # Integer number of full rotations
            
            # Check if we should start easing
            should_ease = False
            
            if self.target_is_close:
                # If target is close to start, do 2 rotations first
                if self.rotation_count >= 2:
                    # Calculate distance from current position to target
                    angle_diff_to_target = (target_angle - current_angle) % 360
                    should_ease = angle_diff_to_target <= 120
            else:
                # If target is far from start, do 3 rotations first
                if self.rotation_count >= 3:
                    # Calculate distance from current position to target
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
                # Use cubic easing out
                ease_progress = 1 - (1 - ease_progress) ** 3
                
                # Calculate target speed (from 360 to 0 degrees per second)
                # Start at 360 and gradually reduce to 0
                target_speed = 360 * (1 - ease_progress)
                # Ensure minimum speed of 30 degrees per second
                target_speed = max(target_speed, 30)
                rotation_this_frame = target_speed * delta_time
                
                # Prevent overshooting
                if rotation_this_frame > angle_diff_to_target:
                    rotation_this_frame = angle_diff_to_target
                
                self.wheel_angle = (self.wheel_angle + rotation_this_frame) % 360
                self.total_rotation += rotation_this_frame
            else:
                # Constant speed of 360 degrees per second
                self.wheel_angle = (self.wheel_angle + rotation_this_frame) % 360

    def check_slots_win(self):
        if len(set(self.slot_results)) == 1:
            multiplier = 5 if self.slot_results[0] == "💎" else 3
            self.game.eggs += self.bet_amount * multiplier

    def check_wheel_win(self):
        current_section = self.get_current_section()
        if current_section:
            winnings = int(self.bet_amount * current_section["multiplier"])  # Round down to whole number
            self.game.eggs += winnings
            print(f"Won {winnings} eggs! ({current_section['name']} - {current_section['multiplier']}x)")

    def handle_mouse_motion(self, event):
        if self.current_game is None:
            for button in self.mode_buttons.values():
                button.handle_event(event)
        else:
            for button in self.bet_buttons.values():
                button.handle_event(event)
            if not (self.spinning or self.wheel_spinning) and self.bet_amount > 0:
                self.spin_button.handle_event(event)
            if self.current_game == "wheel":
                for button in self.debug_buttons.values():
                    button.handle_event(event)

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_game is None:
                for button_name, button in self.mode_buttons.items():
                    if button.handle_event(event):
                        if button_name == "wheel":  # Only allow wheel mode
                            self.current_game = button_name
            else:
                if self.current_game == "wheel":
                    # Handle debug buttons
                    for button_name, button in self.debug_buttons.items():
                        if button.handle_event(event):
                            if button_name == "fine_minus":
                                self.wheel_angle = (self.wheel_angle - 1) % 360
                            elif button_name == "fine_plus":
                                self.wheel_angle = (self.wheel_angle + 1) % 360
                            print(f"Wheel angle: {self.wheel_angle:.1f}°")

                for button_name, button in self.bet_buttons.items():
                    if button.handle_event(event):
                        if button_name == "increase":
                            if self.game.eggs > 0:
                                self.bet_amount = min(self.bet_amount * 2, self.game.eggs)
                        else:
                            self.bet_amount = max(self.bet_amount // 2, 0)
                
                if not (self.spinning or self.wheel_spinning) and self.bet_amount > 0:
                    if self.spin_button.handle_event(event):
                        if self.current_game == "wheel" and self.game.eggs >= self.bet_amount:
                            self.game.eggs -= self.bet_amount
                            self.wheel_spinning = True
                            # Reset target angle when starting a new spin
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