import pygame
import sys


def gambling_menu(screen, font):
    PASTEL_ORANGE = (255, 204, 153)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Set up buttons and background
    back_button_rect = pygame.Rect(10, 10, 150, 50)
    pygame.draw.rect(screen, PASTEL_ORANGE, back_button_rect)
    back_text = font.render("Back to Menu", True, BLACK)
    screen.blit(back_text, (back_button_rect.centerx - back_text.get_width() // 2, back_button_rect.centery - back_text.get_height() // 2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if back_button_rect.collidepoint(x, y):
                    return
