from __future__ import annotations
import logging
import pygame
from enum import Enum
from zelda.sprite.camera import YSortCameraGroup
from zelda.utils import Utilities
from zelda.config import Config

class SpellType(Enum):
    FLAME = 0,
    HEAL = 1,

class Spell(pygame.sprite.Sprite):
    def __init__(self, config: Config, spell_type: SpellType, direction_surfaces: dict[str, pygame.Surface | list[pygame.Surface]],
                 name: str, strength: int, cost: int, groups):
        super().__init__(groups)
        self.groups = groups
        self.name: str = name
        self.spell_type: SpellType = spell_type
        self.strength: int = strength
        self.cost: int = cost
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.particles: list[pygame.Surface] = []
        self.direction_surfaces = direction_surfaces
        self.config = config
        self.animation_time = 0.1
        self.current_frame = 0
        self.dt = 0


    def create(self, surface: pygame.Surface, player_rect: pygame.rect.Rect, direction: str, clock: pygame.time.Clock):
        if self.spell_type == SpellType.FLAME:
            self.particles = Utilities.import_folder('assets/graphics/particles/flame/frames')
        else:
            self.particles = Utilities.import_folder('assets/graphics/particles/heal/frames')

        while self.current_frame < len(self.particles):
            self.dt += clock.tick(self.config.fps) / 1000
            surf = self.particles[self.current_frame]
            logging.info(self.dt)
            logging.info(self.current_frame)
            if self.dt > self.animation_time:
                self.dt = 0
                self.image = surf

                if direction == 'right':
                    self.rect: pygame.rect.Rect = surf.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 0))
                elif direction == 'left':
                    self.rect: pygame.rect.Rect = surf.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 0))
                elif direction == 'down':
                    self.rect: pygame.rect.Rect = surf.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(0, 0))
                elif direction == 'up':
                    self.rect: pygame.rect.Rect = surf.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(0, 0))
                else:
                    self.rect: pygame.rect.Rect = surf.get_rect(center=player_rect.center)

                self.current_frame += 1
                self.groups.add
                super().__init__(self.groups)
                pygame.draw.rect(surf, (255, 0, 0), self.rect)


        """
        for surf in self.particles:
            self.image = surf

            if direction == 'right':
                self.rect: pygame.rect.Rect = surf.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 0))
            elif direction == 'left':
                self.rect: pygame.rect.Rect = surf.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 0))
            elif direction == 'down':
                self.rect: pygame.rect.Rect = surf.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(0, 0))
            elif direction == 'up':
                self.rect: pygame.rect.Rect = surf.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(0, 0))
            else:
                self.rect: pygame.rect.Rect = surf.get_rect(center=player_rect.center)

            surf = pygame.transform.scale2x(surf)
            super().__init__(self.groups)
            pygame.draw.rect(surf, (255, 0, 0), self.rect)
        """


    @staticmethod
    def create_flame(camera: YSortCameraGroup, config: Config):
        direction_surfaces: dict[str, pygame.Surface | list[pygame.Surface]] = {
            "graphic": pygame.image.load('assets/graphics/particles/flame/fire.png').convert_alpha(),
            "particles": Utilities.import_folder('assets/graphics/particles/flame/frames')
        }

        return Spell(config, SpellType.FLAME, direction_surfaces, "flame", 5, 20, camera)

    @staticmethod
    def create_heal(camera: YSortCameraGroup, config: Config):
        direction_surfaces: dict[str, pygame.Surface | list[pygame.Surface]] = {
            "graphic": pygame.image.load('assets/graphics/particles/heal/heal.png').convert_alpha(),
            "particles": Utilities.import_folder('assets/graphics/particles/heal/frames')
        }

        return Spell(config, SpellType.HEAL, direction_surfaces, "heal", 20, 10, camera)

    def update(self) -> None:
        pass

    def destroy(self) -> None:
        self.kill()
