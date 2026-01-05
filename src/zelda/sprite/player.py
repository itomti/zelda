from dataclasses import dataclass
from enum import IntEnum
import pygame
import logging
from zelda.sprite.spell import Spell, SpellInfo
from zelda.sprite.weapon import Weapon, WeaponInfo
from zelda.sprite.entity import Entity
from zelda.config import Config


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
    IDLE = 13
    MOVE = 14
    ATTACK = 15

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
            case 13:
                value = "idle"
            case 14:
                value = "move"
            case 15:
                value = "attack"

        return value


@dataclass
class PlayerInfo:
    weapon_data: list[WeaponInfo]
    spell_data: list[SpellInfo]
    animations: dict[str, list[pygame.Surface]]
    spell: Spell | None = None
    weapon: Weapon | None = None
    is_attacking = False
    is_cycling = False
    attack_cooldown = 400
    attack_time = 0
    cycling_time = 0
    weapon_index = 0
    health = 100
    energy = 60
    magic = 4
    attack = 4
    speed = 6
    experience = 123
    spell_index = 0


class Player(Entity):
    def __init__(self, player_info: PlayerInfo, position, groups: pygame.sprite.Group, obstacle_sprites: pygame.sprite.Group, clock: pygame.time.Clock, config: Config, image: pygame.Surface):
        super().__init__(position, 0.15, 6, image, (0, -26), player_info.animations, obstacle_sprites, groups)
        self.config = config
        self.clock = clock
        self.visible_sprites = groups
        self.image = image
        self.player_info = player_info
        self.status = PlayerAnimationType.DOWN

    def input(self) -> None:
        if self.player_info.is_attacking:
            return

        keys = pygame.key.get_pressed()
        pygame.key.set_repeat()

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

        if keys[pygame.K_SPACE] and not self.player_info.is_attacking:
            self.player_info.is_attacking = True
            self.player_info.attack_time = pygame.time.get_ticks()
            self.attack()

        if keys[pygame.K_LCTRL] and not self.player_info.is_attacking:
            self.player_info.is_attacking = True
            self.player_info.attack_time = pygame.time.get_ticks()
            self.shoot()

        if keys[pygame.K_q] and not self.player_info.is_cycling:
            self.player_info.is_cycling = True
            self.player_info.cycling_time = pygame.time.get_ticks()
            self.player_info.weapon_index += 1
            if self.player_info.weapon_index >= len(self.player_info.weapon_data):
                self.player_info.weapon_index = 0

        if keys[pygame.K_e] and not self.player_info.is_cycling:
            self.player_info.is_cycling = True
            self.player_info.cycling_time = pygame.time.get_ticks()
            self.player_info.spell_index += 1
            if self.player_info.spell_index >= len(self.player_info.spell_data):
                self.player_info.spell_index = 0

    def attack(self):
        data = self.player_info.weapon_data[self.player_info.weapon_index]
        logging.debug(f"Spawning weapon {data.weapon_type}")
        self.player_info.weapon = Weapon(self.rect, data.weapon_type, data.surfaces, data.name, data.cooldown, data.damage, str(self.status).split('_')[0], data.audio, self.visible_sprites)

    def shoot(self):
        data = self.player_info.spell_data[self.player_info.spell_index]
        logging.debug(f"Spawning spell {data.spell_type}")
        self.player_info.spell = Spell(self.rect, self.config, self.clock, data.spell_type, data.spell_image, data.audio, data.particles, data.name, data.strength, data.cost, str(self.status).split('_')[0], self.visible_sprites)

    def update(self) -> None:
        self.input()
        self.reset_is_attacking()
        self.reset_is_cycling()
        self.set_status()
        self.animate()
        self.move()


    def set_status(self) -> None:
        match (self.player_info.is_attacking, self.direction.x, self.direction.y, self.status):
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

        if self.player_info.is_attacking:
            self.direction.x = 0
            self.direction.y = 0

    def animate(self) -> None:
        animation = self.animations[str(self.status)]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image: pygame.surface.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def reset_is_attacking(self) -> None:
        if not self.player_info.is_attacking:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.player_info.attack_time >= self.player_info.attack_cooldown:
            self.player_info.is_attacking = False
            if self.player_info.weapon is not None: self.player_info.weapon.destroy()
            if self.player_info.spell is not None: self.player_info.spell.destroy()

    def reset_is_cycling(self) -> None:
        if not self.player_info.is_cycling:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.player_info.cycling_time >= 200:
            self.player_info.is_cycling = False

