import pygame

import game.sprite.player


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.floor_surface = pygame.image.load('assets/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def draw(self, player: game.sprite.player.Player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_position)

        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
