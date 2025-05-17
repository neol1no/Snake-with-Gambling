import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(40, 40, 40), hover_color=(60, 60, 60)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        self.animation_speed = 0.2
        self.corner_radius = 10
        self.shadow_offset = 3
        self.shadow_color = (20, 20, 20)

    def draw(self, screen):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=self.corner_radius)
        
        # Draw button with current color
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=self.corner_radius)
        
        # Draw border
        border_color = (100, 100, 100) if self.is_hovered else (80, 80, 80)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=self.corner_radius)
        
        # Draw text with shadow
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Text shadow
        shadow_surface = font.render(self.text, True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        screen.blit(shadow_surface, shadow_rect)
        
        # Main text
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.is_hovered
            self.is_hovered = self.rect.collidepoint(event.pos)
            
            # Smooth color transition
            if self.is_hovered and not was_hovered:
                self.target_color = self.hover_color
            elif not self.is_hovered and was_hovered:
                self.target_color = self.color
                
            if hasattr(self, 'target_color'):
                r = self.current_color[0] + (self.target_color[0] - self.current_color[0]) * self.animation_speed
                g = self.current_color[1] + (self.target_color[1] - self.current_color[1]) * self.animation_speed
                b = self.current_color[2] + (self.target_color[2] - self.current_color[2]) * self.animation_speed
                self.current_color = (int(r), int(g), int(b))
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False 