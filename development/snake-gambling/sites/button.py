import pygame

class Button:
    def __init__(self, x, y, width, height, text, game, color=(40, 40, 40), hover_color=(60, 60, 60)):
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
        self.game = game

    def draw(self, screen):
        scale_x = self.game.scale_x
        scale_y = self.game.scale_y
        

        scaled_rect = pygame.Rect(
            int(self.rect.x * scale_x),
            int(self.rect.y * scale_y),
            int(self.rect.width * scale_x),
            int(self.rect.height * scale_y)
        )
        

        shadow_rect = scaled_rect.copy()
        shadow_rect.x += int(self.shadow_offset * scale_x)
        shadow_rect.y += int(self.shadow_offset * scale_y)
        pygame.draw.rect(screen, self.shadow_color, shadow_rect, border_radius=int(self.corner_radius * min(scale_x, scale_y)))
        

        pygame.draw.rect(screen, self.current_color, scaled_rect, border_radius=int(self.corner_radius * min(scale_x, scale_y)))

        border_color = (100, 100, 100) if self.is_hovered else (80, 80, 80)
        pygame.draw.rect(screen, border_color, scaled_rect, int(2 * min(scale_x, scale_y)), border_radius=int(self.corner_radius * min(scale_x, scale_y)))

        font = pygame.font.Font(None, int(36 * min(scale_x, scale_y)))
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=scaled_rect.center)

        shadow_surface = font.render(self.text, True, (0, 0, 0))
        shadow_rect = text_rect.copy()
        shadow_rect.x += int(1 * scale_x)
        shadow_rect.y += int(1 * scale_y)
        screen.blit(shadow_surface, shadow_rect)

        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        scale_x = self.game.scale_x
        scale_y = self.game.scale_y

        scaled_rect = pygame.Rect(
            int(self.rect.x * scale_x),
            int(self.rect.y * scale_y),
            int(self.rect.width * scale_x),
            int(self.rect.height * scale_y)
        )
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = scaled_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False 