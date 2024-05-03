import pygame
from game.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.sprite_type = sprite_type
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(0, -10)