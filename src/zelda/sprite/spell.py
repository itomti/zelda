from __future__ import annotations
import logging
import pygame
from enum import Enum
from zelda.config import Config

class SpellType(Enum):
    FLAME = 0,
    HEAL = 1,

class Spell(pygame.sprite.Sprite):
    def __init__(self, player_rect: pygame.rect.Rect, config: Config, clock: pygame.time.Clock, spell_type: SpellType, spell_image: pygame.Surface, spell_audio: pygame.mixer.Sound, particles: list[pygame.Surface],
                 name: str, strength: int, cost: int, direction: str, groups):
        super().__init__(groups)
        self.clock = clock
        self.player_rect = player_rect
        self.name: str = name
        self.spell_type: SpellType = spell_type
        self.strength: int = strength
        self.cost: int = cost
        self.spell_image: pygame.Surface = spell_image
        self.particles: list[pygame.Surface] = particles
        self.image = particles[0]
        self.rect: pygame.rect.Rect = pygame.rect.Rect(0, 0, 0, 0)
        self.particles: list[pygame.Surface] = particles
        self.audio: pygame.mixer.Sound = spell_audio
        self.config = config
        self.animation_speed = 0.1
        self.current_frame = 0
        self.dt = 0
        self.direction: str = direction
        self.offset = 0
        self.audio.play()


    def display(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.particles):
            self.current_frame = 0
            self.audio.stop()

        self.image: pygame.surface.Surface = self.particles[int(self.current_frame)]
        if self.direction == 'right':
            self.rect: pygame.rect.Rect = self.image.get_rect(midleft=self.player_rect.midright + pygame.math.Vector2(0 + self.offset, 16))
        elif self.direction == 'left':
            self.rect: pygame.rect.Rect = self.image.get_rect(midright=self.player_rect.midleft + pygame.math.Vector2(0 - self.offset, 16))
        elif self.direction == 'down':
            self.rect: pygame.rect.Rect = self.image.get_rect(midtop=self.player_rect.midbottom + pygame.math.Vector2(16, 0 + self.offset))
        elif self.direction == 'up':
            self.rect: pygame.rect.Rect = self.image.get_rect(midbottom=self.player_rect.midtop + pygame.math.Vector2(16, 0 - self.offset))
        else:
            self.rect: pygame.rect.Rect = self.image.get_rect(center=self.player_rect.center)

        self.offset += 2

    def update(self):
        self.display()

    def destroy(self) -> None:
        self.kill()
