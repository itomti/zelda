from __future__ import annotations
import pygame
from enum import Enum
from zelda.sprite.camera import YSortCameraGroup

class WeaponType(Enum):
    SWORD = 0,
    SAI = 1,
    RAPIER = 2,
    LANCE = 3,
    AXE = 4

class Direction(Enum):
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3

class Weapon(pygame.sprite.Sprite):
    def __init__(self, weapon_type: WeaponType, direction_surfaces: dict[str, pygame.Surface],
                 name: str, cooldown: int, damage: int, groups):
        super().__init__(groups)
        self.groups = groups
        self.weapon_type: WeaponType = weapon_type
        self.cooldown: int = cooldown
        self.damage: int = damage
        self.name: str = name
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.direction_surfaces = direction_surfaces

    def create_weapon(self, surface: pygame.Surface, player_rect: pygame.rect.Rect, direction: str) -> None:
        self.image: pygame.surface.Surface = self.direction_surfaces[direction]
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

        super().__init__(self.groups[0])
        pygame.draw.rect(self.image, (255, 0, 0), self.rect, 2)

    @staticmethod
    def create_axe(camera: YSortCameraGroup) -> Weapon:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/axe/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/axe/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/axe/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/axe/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/axe/full.png').convert_alpha()
        }
        return Weapon(WeaponType.AXE, direction_surfaces, "axe", 300, 20, camera)

    @staticmethod
    def create_lance(camera: YSortCameraGroup) -> Weapon:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/lance/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/lance/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/lance/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/lance/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/lance/full.png').convert_alpha()
        }
        return Weapon(WeaponType.LANCE, direction_surfaces, "lance", 400, 30, camera)

    @staticmethod
    def create_rapier(camera: YSortCameraGroup) -> Weapon:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/rapier/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/rapier/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/rapier/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/rapier/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/rapier/full.png').convert_alpha()
        }
        return Weapon(WeaponType.RAPIER, direction_surfaces, "rapier", 300, 20, camera)

    @staticmethod
    def create_sai(camera: YSortCameraGroup) -> Weapon:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/sai/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/sai/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/sai/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/sai/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/sai/full.png').convert_alpha()
        }
        return Weapon(WeaponType.SAI, direction_surfaces, "sai", 80, 10, camera)

    @staticmethod
    def create_sword(camera: YSortCameraGroup) -> Weapon:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/sword/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/sword/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/sword/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/sword/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/sword/full.png').convert_alpha()
        }
        return Weapon(WeaponType.SWORD, direction_surfaces, "sword", 80, 10, camera)

    def destroy(self):
        self.kill()
