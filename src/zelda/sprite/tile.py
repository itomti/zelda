import pygame

from zelda.config import Config

class Tile(pygame.sprite.Sprite):
    def __init__(self, config: Config, position, groups, sprite_type, surface: pygame.Surface | None = None):
        super().__init__(groups)
        self.config = config
        if surface is None:
            self.image = pygame.Surface((config.tile_size, config.tile_size))
        else:
            self.image = surface
        self.sprite_type = sprite_type
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - self.config.tile_size))
        else:
            self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(0, -10)
