from dataclasses import dataclass
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
        self.move_cooldown = 5000
        self.move_time = pygame.time.get_ticks()
        self.is_moving = False
        self.times_moved = 0
        self.times_to_move = 0
        self.can_move: bool = True

    def update(self):
        self.animate()
        self.reset_moving()
        self.move()


    def reset_moving(self) -> None:
        if self.is_moving and self.times_moved != self.times_to_move:
            self.times_moved += 1
            return

        self.times_moved = 0
        self.times_to_move = 0
        self.is_moving = False
        self.can_move = True
        self.direction.x = 0
        self.direction.y = 0

    def random_move(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time - self.move_time <= self.move_cooldown:
            return

        self.times_to_move = random.randint(64, 128)
        self.status = AnimationType.MOVE
        self.move_time = pygame.time.get_ticks()
        self.pick_direction()
        self.can_move = False
        self.is_moving = True

    def pick_direction(self) -> None:
        if self.is_moving:
            return

        random_direction = random.randint(0, 3)

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
