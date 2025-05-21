import pygame
import math

class Button:
    def __init__(self, x, y, width, height, text, game, color=(100, 100, 100), hover_color=(150, 150, 150)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.game = game

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
        self.selection_x = 0
        self.target_x = 0
        self.animation_speed = 0.2

    def load_images(self):
        self.wasd_image = pygame.image.load("assets/WASD.png")
        self.arrow_image = pygame.image.load("assets/ARROW.png")
        self.wasd_image = pygame.transform.scale(self.wasd_image, (100, 100))
        self.arrow_image = pygame.transform.scale(self.arrow_image, (100, 100))

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        center_x = self.game.display_width // 2 - button_width // 2
        
        self.buttons = {
            "back": Button(center_x, self.game.height - 100, button_width, button_height, "Back", self.game)
        }

    def draw(self, screen):
        screen.fill((20, 20, 20))
        
        title_font = pygame.font.Font(None, int(74 * min(self.game.scale_x, self.game.scale_y)))
        title_text = title_font.render("Settings", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.display_width//2, int(200 * self.game.scale_y)))
        screen.blit(title_text, title_rect)
        
        box_width = int(220 * self.game.scale_x)
        box_height = int(120 * self.game.scale_y)
        input_x = self.game.display_width // 2 - box_width // 2
        input_y = int(300 * self.game.scale_y)
        
        pygame.draw.rect(screen, (40, 40, 40), (input_x, input_y, box_width, box_height), border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
        pygame.draw.rect(screen, (255, 255, 255), (input_x, input_y, box_width, box_height), 2, border_radius=int(15 * min(self.game.scale_x, self.game.scale_y)))
        
        wasd_size = int(100 * min(self.game.scale_x, self.game.scale_y))
        arrow_size = int(100 * min(self.game.scale_x, self.game.scale_y))
        scaled_wasd = pygame.transform.scale(self.wasd_image, (wasd_size, wasd_size))
        scaled_arrow = pygame.transform.scale(self.arrow_image, (arrow_size, arrow_size))
        
        wasd_rect = scaled_wasd.get_rect(topleft=(input_x + int(10 * self.game.scale_x), input_y + int(10 * self.game.scale_y)))
        screen.blit(scaled_wasd, wasd_rect)
        
        arrow_rect = scaled_arrow.get_rect(topleft=(input_x + int(110 * self.game.scale_x), input_y + int(10 * self.game.scale_y)))
        screen.blit(scaled_arrow, arrow_rect)
        
        target_x = input_x + int(110 * self.game.scale_x) if self.game.use_arrow_keys else input_x + int(10 * self.game.scale_x)
        self.selection_x += (target_x - self.selection_x) * self.animation_speed
        
        indicator_width = int(100 * self.game.scale_x)
        indicator_height = int(100 * self.game.scale_y)
        indicator_rect = pygame.Rect(self.selection_x, input_y + int(10 * self.game.scale_y), indicator_width, indicator_height)
        pygame.draw.rect(screen, (0, 255, 0, 128), indicator_rect, 2, border_radius=int(10 * min(self.game.scale_x, self.game.scale_y)))
        
        self.buttons["back"].draw(screen)
        
        font = pygame.font.Font(None, int(36 * min(self.game.scale_x, self.game.scale_y)))
        back_text = font.render("Press ESC to return", True, (255, 255, 255))
        back_rect = back_text.get_rect(center=(self.game.display_width//2, self.game.display_height - int(50 * self.game.scale_y)))
        back_shadow = font.render("Press ESC to return", True, (0, 0, 0))
        screen.blit(back_shadow, (back_rect.x + 2, back_rect.y + 2))
        screen.blit(back_text, back_rect)

    def handle_input(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons.values():
                button.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            box_width = int(220 * self.game.scale_x)
            input_x = self.game.display_width // 2 - box_width // 2
            input_y = int(300 * self.game.scale_y)
            mouse_pos = pygame.mouse.get_pos()
            
            wasd_rect = pygame.Rect(input_x + int(10 * self.game.scale_x), input_y + int(10 * self.game.scale_y), 
                                  int(100 * self.game.scale_x), int(100 * self.game.scale_y))
            if wasd_rect.collidepoint(mouse_pos):
                self.game.use_arrow_keys = False
                return
                
            arrow_rect = pygame.Rect(input_x + int(110 * self.game.scale_x), input_y + int(10 * self.game.scale_y), 
                                   int(100 * self.game.scale_x), int(100 * self.game.scale_y))
            if arrow_rect.collidepoint(mouse_pos):
                self.game.use_arrow_keys = True
                return
            
            for button_name, button in self.buttons.items():
                if button.handle_event(event):
                    if button_name == "back":
                        self.game.game_state = self.game.previous_state 