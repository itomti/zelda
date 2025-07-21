import logging
import pygame
from enum import Enum, IntEnum
from zelda.sprite.spell import Spell
from zelda.sprite.weapon import Weapon
from zelda.utils import Utilities
from zelda.config import Config

class DirectionType(Enum):
    HORIZONTAL = 1,
    VERTICAL = 2


class PlayerAnimationType(IntEnum):
    DOWN = 1
    DOWN_ATTACK = 2
    DOWN_IDLE = 3
    LEFT = 4
    LEFT_ATTACK = 5
    LEFT_IDLE = 6
    RIGHT = 7
    RIGHT_ATTACK = 8
    RIGHT_IDLE = 9
    UP = 10
    UP_ATTACK = 11
    UP_IDLE = 12

    def __str__(self):
        value = ""
        match self.value:
            case 1:
                value = "down"
            case 2:
                value = "down_attack"
            case 3:
                value = "down_idle"
            case 4:
                value = "left"
            case 5:
                value = "left_attack"
            case 6:
                value = "left_idle"
            case 7:
                value = "right"
            case 8:
                value = "right_attack"
            case 9:
                value = "right_idle"
            case 10:
                value = "up"
            case 11:
                value = "up_attack"
            case 12:
                value = "up_idle"

        return value

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups: pygame.sprite.Group, obstacle_sprites: pygame.sprite.Group, clock: pygame.time.Clock, config: Config, animations: dict[str, list[pygame.Surface]]):
        super().__init__(groups)
        self.config = config
        self.clock = clock
        # sprites
        self.visible_sprites = groups
        self.image = pygame.image.load("assets/graphics/player/down/down_0.png").convert_alpha()
        self.animations = animations

        # rects
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.hit_box = self.rect.inflate(0, -26)

        # animation info
        self.is_attacking = False
        self.is_cycling = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.cycling_time = 0
        self.status: PlayerAnimationType = PlayerAnimationType.DOWN
        self.frame_index: float = 0
        self.animation_speed: float = 0.15

        # weapon
        self.weapon_index = 0
        self.weapon_data = Utilities.import_weapon_data()
        self.weapon: Weapon | None = None

        # stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.experience = 123

        # magic
        self.spell_index = 0
        self.spell_data = Utilities.import_magic_data()
        self.spell: Spell | None = None

    def input(self) -> None:
        if self.is_attacking:
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = PlayerAnimationType.UP
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = PlayerAnimationType.DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = PlayerAnimationType.RIGHT
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = PlayerAnimationType.LEFT
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
        data = self.weapon_data[self.weapon_index]
        self.weapon = Weapon(self.rect, data['type'], data['surfaces'], data['name'], data['cooldown'], data['damage'], str(self.status).split('_')[0], self.visible_sprites)

    def shoot(self):
        data = self.spell_data[self.spell_index]
        self.spell = Spell(self.rect, self.config, self.clock, data['type'], data['image'], data['particles'], data['name'], data['strength'], data['cost'], str(self.status).split('_')[0], self.visible_sprites)

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
        animation = self.animations[str(self.status)]
        logging.info(str(self.status))
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image: pygame.surface.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def set_status(self) -> None:
        """
        x == 0: ??
        x == 1: right
        x == -1: left
        y == 0: ??
        y == 1: down
        y == -1: up
        """

        match (self.is_attacking, self.direction.x, self.direction.y, self.status):
            case (False, 0, 0, PlayerAnimationType.LEFT):
                self.status = PlayerAnimationType.LEFT_IDLE
            case (False, 0, 0, PlayerAnimationType.UP):
                self.status = PlayerAnimationType.UP_IDLE
            case (False, 0, 0, PlayerAnimationType.RIGHT):
                self.status = PlayerAnimationType.RIGHT_IDLE
            case (False, 0, 0, PlayerAnimationType.DOWN):
                self.status = PlayerAnimationType.DOWN_IDLE
            case (True, -1, 0, PlayerAnimationType.LEFT) if PlayerAnimationType.LEFT == self.status:
                self.status = PlayerAnimationType.LEFT_ATTACK
            case (True, 0, -1, PlayerAnimationType.UP) if PlayerAnimationType.UP == self.status:
                self.status = PlayerAnimationType.UP_ATTACK
            case (True, 1, 0, PlayerAnimationType.RIGHT) if PlayerAnimationType.RIGHT == self.status:
                self.status = PlayerAnimationType.RIGHT_ATTACK
            case (True, 0, 1, PlayerAnimationType.DOWN) if PlayerAnimationType.DOWN == self.status:
                self.status = PlayerAnimationType.DOWN_ATTACK
            case (True, _, _, PlayerAnimationType.LEFT_IDLE) if PlayerAnimationType.LEFT_IDLE == self.status:
                self.status = PlayerAnimationType.LEFT_ATTACK
            case (True, _, _, PlayerAnimationType.UP_IDLE) if PlayerAnimationType.UP_IDLE == self.status:
                self.status = PlayerAnimationType.UP_ATTACK
            case (True, _, _, PlayerAnimationType.RIGHT_IDLE) if PlayerAnimationType.RIGHT_IDLE == self.status:
                self.status = PlayerAnimationType.RIGHT_ATTACK
            case (True, _, _, PlayerAnimationType.DOWN_IDLE) if PlayerAnimationType.DOWN_IDLE == self.status:
                self.status = PlayerAnimationType.DOWN_ATTACK
            case (False, _, _, PlayerAnimationType.LEFT_ATTACK):
                self.status = PlayerAnimationType.LEFT_IDLE
            case (False, _, _, PlayerAnimationType.UP_ATTACK):
                self.status = PlayerAnimationType.UP_IDLE
            case (False, _, _, PlayerAnimationType.RIGHT_ATTACK):
                self.status = PlayerAnimationType.RIGHT_IDLE
            case (False, _, _, PlayerAnimationType.DOWN_ATTACK):
                self.status = PlayerAnimationType.DOWN_IDLE

        if self.is_attacking:
            self.direction.x = 0
            self.direction.y = 0


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
