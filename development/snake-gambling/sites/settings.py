import pygame
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

class Settings:
    def __init__(self, game):
        self.game = game
        self.setup_buttons()
        self.load_images()
        self.selection_x = 0  # For smooth sliding animation
        self.target_x = 0    # Target position for selection
        self.animation_speed = 0.2  # Speed of the sliding animation

    def load_images(self):
        self.wasd_image = pygame.image.load("assets/WASD.png")
        self.arrow_image = pygame.image.load("assets/ARROW.png")
        self.wasd_image = pygame.transform.scale(self.wasd_image, (100, 100))
        self.arrow_image = pygame.transform.scale(self.arrow_image, (100, 100))

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.game.width // 2 - button_width // 2
        
        self.buttons = {
            "debug_toggle": Button(center_x, 300, button_width, button_height, "Debug Mode: OFF"),
            "back": Button(center_x, 440, button_width, button_height, "Back")
        }

    def draw(self, screen):
        screen.fill((20, 20, 20))
        
        # Draw title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.width//2, 200))
        screen.blit(title_text, title_rect)
        
        # Draw debug toggle button
        self.buttons["debug_toggle"].draw(screen)
        
        # Draw control switch
        box_width = 220
        box_height = 120
        input_x = self.game.width // 2 - box_width // 2
        input_y = 300
        
        # Draw background for input switch with rounded corners
        pygame.draw.rect(screen, (40, 40, 40), (input_x, input_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), (input_x, input_y, box_width, box_height), 2, border_radius=15)
        
        # Draw WASD image
        wasd_rect = self.wasd_image.get_rect(topleft=(input_x + 10, input_y + 10))
        screen.blit(self.wasd_image, wasd_rect)
        
        # Draw Arrow image
        arrow_rect = self.arrow_image.get_rect(topleft=(input_x + 110, input_y + 10))
        screen.blit(self.arrow_image, arrow_rect)
        
        # Update selection position
        target_x = input_x + 110 if self.game.use_arrow_keys else input_x + 10
        self.selection_x += (target_x - self.selection_x) * self.animation_speed
        
        # Draw selection indicator
        indicator_width = 100
        indicator_height = 100
        indicator_rect = pygame.Rect(self.selection_x, input_y + 10, indicator_width, indicator_height)
        pygame.draw.rect(screen, (0, 255, 0, 128), indicator_rect, 2, border_radius=10)
        
        # Draw back button
        self.buttons["back"].draw(screen)

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.values():
                button.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check for input method switch clicks
            box_width = 220
            input_x = self.game.width // 2 - box_width // 2
            input_y = 300
            mouse_pos = pygame.mouse.get_pos()
            
            # Check WASD area
            wasd_rect = pygame.Rect(input_x + 10, input_y + 10, 100, 100)
            if wasd_rect.collidepoint(mouse_pos):
                self.game.use_arrow_keys = False
                return
                
            # Check Arrow area
            arrow_rect = pygame.Rect(input_x + 110, input_y + 10, 100, 100)
            if arrow_rect.collidepoint(mouse_pos):
                self.game.use_arrow_keys = True
                return
            
            # Check other buttons
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    if button_name == "debug_toggle":
                        self.game.debug_mode = not self.game.debug_mode
                        button.text = f"Debug Mode: {'ON' if self.game.debug_mode else 'OFF'}"
                    elif button_name == "back":
                        self.game.game_state = self.game.previous_state 