from __future__ import annotations
from dataclasses import dataclass
import pathlib
import pygame
from enum import Enum
from zelda.sprite.camera import YSortCameraGroup

class WeaponType(Enum):
    SWORD = 0
    SAI = 1
    RAPIER = 2
    LANCE = 3
    AXE = 4
    UNKNOWN = 5

    def __str__(self) -> str:
        value = ""

        match self.value:
            case 0:
                value = "Sword"
            case 1:
                value = "Sai"
            case 2:
                value = "Rapier"
            case 3:
                value = "Lance"
            case 4:
                value = "Axe"
            case _:
                value = f"Unknown, val: {self.value}"

        return value

class Direction(Enum):
    LEFT = 0,
    UP = 1,
    RIGHT = 2,
    DOWN = 3

@dataclass
class WeaponInfo:
    weapon_type: WeaponType
    cooldown: int
    damage: int
    name: str
    surfaces: dict[str, pygame.Surface]
    audio: pygame.mixer.Sound
    image: pygame.Surface

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: pygame.rect.Rect, weapon_type: WeaponType, direction_surfaces: dict[str, pygame.Surface],
                 name: str, cooldown: int, damage: int, direction: str, audio: pygame.mixer.Sound, groups):
        super().__init__(groups)
        self.weapon_type: WeaponType = weapon_type
        self.cooldown: int = cooldown
        self.damage: int = damage
        self.name: str = name
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.direction_surfaces = direction_surfaces
        self.player_rect: pygame.rect.Rect = player
        self.direction: str = direction
        self.audio: pygame.mixer.Sound = audio
        self.audio.play()

    def display(self) -> None:
        self.image: pygame.surface.Surface = self.direction_surfaces[self.direction]
        if self.direction == 'right':
            self.rect: pygame.rect.Rect = self.image.get_rect(midleft=self.player_rect.midright + pygame.math.Vector2(0, 16))
        elif self.direction == 'left':
            self.rect: pygame.rect.Rect = self.image.get_rect(midright=self.player_rect.midleft + pygame.math.Vector2(0, 16))
        elif self.direction == 'down':
            self.rect: pygame.rect.Rect = self.image.get_rect(midtop=self.player_rect.midbottom + pygame.math.Vector2(16, 0))
        elif self.direction == 'up':
            self.rect: pygame.rect.Rect = self.image.get_rect(midbottom=self.player_rect.midtop + pygame.math.Vector2(16, 0))
        else:
            self.rect: pygame.rect.Rect = self.image.get_rect(center=self.player_rect.center)



    @staticmethod
    def create_axe() -> WeaponInfo:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/axe/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/axe/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/axe/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/axe/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/axe/full.png').convert_alpha()
        }

        audio = pygame.mixer.Sound("assets/audio/slash.wav")
        image = pygame.image.load('assets/weapons/axe/full.png').convert_alpha()
        return WeaponInfo(WeaponType.AXE, 300, 20, 'axe', direction_surfaces, audio, image)

    @staticmethod
    def create_lance() -> WeaponInfo:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/lance/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/lance/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/lance/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/lance/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/lance/full.png').convert_alpha()
        }

        audio = pygame.mixer.Sound("assets/audio/claw.wav")
        image = pygame.image.load('assets/weapons/lance/full.png').convert_alpha()
        return WeaponInfo(WeaponType.LANCE, 300, 20, 'lance', direction_surfaces, audio, image)


    @staticmethod
    def create_rapier() -> WeaponInfo:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/rapier/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/rapier/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/rapier/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/rapier/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/rapier/full.png').convert_alpha()
        }

        audio = pygame.mixer.Sound("assets/audio/claw.wav")
        image = pygame.image.load('assets/weapons/rapier/full.png').convert_alpha()
        return WeaponInfo(WeaponType.RAPIER, 300, 20, 'rapier', direction_surfaces, audio, image)

    @staticmethod
    def create_sai() -> WeaponInfo:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/sai/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/sai/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/sai/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/sai/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/sai/full.png').convert_alpha()
        }

        audio = pygame.mixer.Sound("assets/audio/slash.wav")
        image = pygame.image.load('assets/weapons/sai/full.png').convert_alpha()
        return WeaponInfo(WeaponType.SAI, 80, 10, 'sai', direction_surfaces, audio, image)


    @staticmethod
    def create_sword() -> WeaponInfo:
        direction_surfaces: dict[str, pygame.Surface] = {
            'left': pygame.image.load('assets/weapons/sword/left.png').convert_alpha(),
            'up': pygame.image.load('assets/weapons/sword/up.png').convert_alpha(),
            'right': pygame.image.load('assets/weapons/sword/right.png').convert_alpha(),
            'down': pygame.image.load('assets/weapons/sword/down.png').convert_alpha(),
            'full': pygame.image.load('assets/weapons/sword/full.png').convert_alpha()
        }

        audio = pygame.mixer.Sound("assets/audio/sword.wav")
        image = pygame.image.load('assets/weapons/sword/full.png').convert_alpha()
        return WeaponInfo(WeaponType.SWORD, 80, 10, 'sword', direction_surfaces, audio, image)


    def update(self):
        self.display()

    def destroy(self):
        self.kill()
