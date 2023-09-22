import pygame
from .config import BLACK, WHITE, DARK_BLUE

class Textbox:
    def __init__(self, pos_rect, text, font, active) -> None:
        self.pos_rect = pos_rect
        self.text = text
        self.active = active
        self.font = font

    def draw(self, screen: pygame.display):
        text_object = self.font.render(self.text, True, WHITE)
        bg_object = pygame.draw.rect(screen, DARK_BLUE, self.pos_rect, width=0)
        rect_object = pygame.draw.rect(screen, WHITE, self.pos_rect, width=2, border_radius=3)
        text_rect = text_object.get_rect(x=rect_object.x, y=rect_object.y)
        screen.blit(text_object,text_rect)