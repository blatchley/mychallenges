import pygame

from .sprites import Item
from .config import BLACK, WHITE, DARK_BLUE


class Itembox:
    def __init__(self, game, pos_rect, active, font) -> None:
        self.game = game
        self.pos_rect = pos_rect
        self.active = active
        self.text = ""
        self.font = font

        self.active_item = ""
        self.active_amount = 0

    def draw(self, screen):
        bg_object = pygame.draw.rect(screen, DARK_BLUE, self.pos_rect, width=0)
        rect_object = pygame.draw.rect(screen, WHITE, self.pos_rect, width=2, border_radius=3)

        if self.active_item == "key":
            sp = self.game.terrain_spritesheet.get_sprite(64,960,32,32)
        elif self.active_item == "cool_sunglasses":
            sp = self.game.terrain_spritesheet.get_sprite(96,960,32,32)
        else:
            return
        
        sp = pygame.transform.scale(sp, (64, 64))
        self.game.screen.blit(sp, self.pos_rect)

        text_object = self.font.render(f"x{self.active_amount}", True, WHITE)
        text_rect = text_object.get_rect(x=rect_object.x, y=rect_object.y)
        screen.blit(text_object,text_rect)
        