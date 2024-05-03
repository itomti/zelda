import pygame
import game.settings
from enum import Enum


class WeaponType(Enum):
    SWORD = 0,
    SAI = 1,
    RAPIER = 2,
    LANCE = 3,
    AXE = 4


class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, weapon_data: dict):
        super().__init__(groups)
        self.cooldown = weapon_data['cooldown']
        self.damage = weapon_data['damage']
        self.weapon_data = weapon_data
        self.rect = None
        self.image = None

    def create_weapon(self, player_rect: pygame.rect.Rect, direction: str) -> None:
        self.image: pygame.surface.Surface = self.weapon_data['direction_surfaces'][direction]
        if direction == 'right':
            self.rect: pygame.rect.Rect = self.image.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect: pygame.rect.Rect = self.image.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect: pygame.rect.Rect = self.image.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(16, 0))
        elif direction == 'up':
            self.rect: pygame.rect.Rect = self.image.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(16, 0))
        else:
            self.rect: pygame.rect.Rect = self.image.get_rect(center=player_rect.center)

    def destroy(self):
        self.kill()