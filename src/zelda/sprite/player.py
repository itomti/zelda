import logging
import pygame
from enum import Enum
from zelda.settings import *
from zelda.sprite.spell import Spell
from zelda.utils import Utilities

class DirectionType(Enum):
    HORIZONTAL = 1,
    VERTICAL = 2


class PlayerAnimationType(Enum):
    DOWN = 1,
    DOWN_ATTACK = 2,
    DOWN_IDLE = 3,
    LEFT = 4,
    LEFT_ATTACK = 5,
    LEFT_IDLE = 6,
    RIGHT = 7,
    RIGHT_ATTACK = 8,
    RIGHT_IDLE = 9,
    UP = 10,
    UP_ATTACK = 11
    UP_IDLE = 12


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups: pygame.sprite.Group, obstacle_sprites: pygame.sprite.Group):
        super().__init__(groups)
        # sprites
        self.visible_sprites = groups
        self.image = pygame.image.load("assets/graphics/test/player.png").convert_alpha()
        self.animations = {}
        self.import_player_assets()

        # rects
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.hit_box = self.rect.inflate(0, -26)

        # animation info
        self.is_attacking = False
        self.is_cycling = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.cycling_time = None
        self.status: str = 'down'
        self.frame_index: float = 0
        self.animation_speed: float = 0.15

        # weapon
        self.weapon_index = 0
        self.weapon_data = import_weapon_data(self.visible_sprites)
        self.weapon = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.experience = 123

        # magic
        self.spell_index = 0
        self.spell_data = import_magic_data(self.visible_sprites)
        self.spell = None

    def import_player_assets(self):
        character_path = 'assets/graphics/player'
        self.animations = {
            'left': [],
            'left_attack': [],
            'left_idle': [],
            'up': [],
            'up_attack': [],
            'up_idle': [],
            'right': [],
            'right_attack': [],
            'right_idle': [],
            'down': [],
            'down_attack': [],
            'down_idle': []
        }
        for animation in self.animations.keys():
            folder_path: str = f"{character_path}/{animation}"
            surfaces = Utilities.import_folder(folder_path)
            self.animations[animation] = surfaces

    def input(self) -> None:
        if self.is_attacking:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack()

        if keys[pygame.K_LCTRL] and not self.is_attacking:
            self.is_attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.shoot()

        if keys[pygame.K_q] and not self.is_cycling:
            self.is_cycling = True
            self.cycling_time = pygame.time.get_ticks()
            self.weapon_index += 1
            if self.weapon_index >= len(self.weapon_data):
                self.weapon_index = 0

        if keys[pygame.K_e] and not self.is_cycling:
            self.is_cycling = True
            self.cycling_time = pygame.time.get_ticks()
            self.spell_index += 1
            if self.spell_index >= len(self.spell_data):
                self.spell_index = 0

    def attack(self):
        self.weapon = self.weapon_data[self.weapon_index]
        self.weapon.create_weapon(pygame.display.get_surface(), self.rect, self.status.split('_')[0])

    def shoot(self):
        self.spell = self.spell_data[self.spell_index]
        self.spell.create(pygame.display.get_surface(), self.rect, self.status.split('_')[0])

    def collision(self, direction: DirectionType):
        if direction == DirectionType.HORIZONTAL:
            for sprite in self.obstacle_sprites:
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.x > 0:
                        self.hit_box.right = sprite.hit_box.left
                    elif self.direction.x < 0:
                        self.hit_box.left = sprite.hit_box.right

        if direction == DirectionType.VERTICAL:
            for sprite in self.obstacle_sprites:
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.y > 0:
                        self.hit_box.bottom = sprite.hit_box.top
                    elif self.direction.y < 0:
                        self.hit_box.top = sprite.hit_box.bottom

    def move(self) -> None:
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hit_box.x += self.direction.x * self.speed
        self.collision(DirectionType.HORIZONTAL)
        self.hit_box.y += self.direction.y * self.speed
        self.collision(DirectionType.VERTICAL)
        self.rect.center = self.hit_box.center

    def update(self) -> None:
        self.input()
        self.reset_is_attacking()
        self.reset_is_cycling()
        self.set_status()
        self.animate()
        self.move()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image: pygame.surface.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def set_status(self) -> None:
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status:
                self.status = self.status.replace('_attack', '')
                self.status = self.status + '_idle'

        if self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                self.status = self.status.replace('_idle', '')
                self.status = self.status + '_attack'
        else:
            self.status = self.status.replace('_attack', '')

    def reset_is_attacking(self) -> None:
        if not self.is_attacking:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.is_attacking = False
            if self.weapon is not None: self.weapon.destroy()
            if self.spell is not None: self.spell.destroy()

    def reset_is_cycling(self) -> None:
        if not self.is_cycling:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.cycling_time >= 200:
            self.is_cycling = False
