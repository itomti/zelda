from dataclasses import dataclass
import pygame
from zelda.sprite.entity import Entity

@dataclass
class EnemyInfo:
    name: str
    health: int
    experience: int
    damage: int
    attack_type: str
    attack_sound: pygame.mixer.Sound
    image: pygame.Surface

class Enemy(Entity):
    def __init__(self, position: tuple, enemy_info: EnemyInfo, obstacles, sprites):
        super().__init__(position, 0.15, 0.15, enemy_info.image, (0, -26), {}, obstacles, sprites)
        self.info = enemy_info
        self.image = enemy_info.image
        self.visible_sprites = sprites
