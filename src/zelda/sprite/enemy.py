from dataclasses import dataclass
from enum import IntEnum
import random
import logging
import pygame
from zelda.sprite.entity import Entity, AnimationType

@dataclass
class EnemyInfo:
    name: str
    health: int
    experience: int
    damage: int
    attack_type: str
    attack_sound: pygame.mixer.Sound
    image: pygame.Surface
    animations: dict[str, list[pygame.Surface]]

class Enemy(Entity):
    def __init__(self, position: tuple, enemy_info: EnemyInfo, obstacles, sprites):
        super().__init__(position, 0.15, 1.5, enemy_info.image, (0, -26), enemy_info.animations, AnimationType.IDLE, obstacles, sprites)
        self.info = enemy_info
        self.image = enemy_info.image
        self.visible_sprites = sprites
        self.status = AnimationType.IDLE
        self.move_cooldown = 3000
        self.move_time = pygame.time.get_ticks()

    def update(self):
        self.animate()
        self.random_move()

    def random_move(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.move_time <= self.move_cooldown:
            return

        self.move_time = pygame.time.get_ticks()
        random_direction = random.randint(0, 3)
        times_to_move = random.randint(0, 15)
        self.status = AnimationType.MOVE
        logging.info(f"moving {times_to_move} time(s)")

        if random_direction == 0:
            self.direction.y = 0
            self.direction.x = -1
        elif random_direction == 1:
            self.direction.x = 0
            self.direction.y = -1
        elif random_direction == 2:
            self.direction.x = 1
            self.direction.y = 0
        elif random_direction == 3:
            self.direction.x = 0
            self.direction.y = 1

        for _ in range(times_to_move):
            self.move()

        self.direction.x = 0
        self.direction.y = 0
