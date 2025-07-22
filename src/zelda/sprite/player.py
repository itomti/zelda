from dataclasses import dataclass
import pygame
import logging
from zelda.sprite.spell import Spell, SpellInfo
from zelda.sprite.weapon import Weapon
from zelda.sprite.entity import Entity, AnimationType
from zelda.utils import Utilities
from zelda.config import Config

class Player(Entity):
    def __init__(self, position, groups: pygame.sprite.Group, obstacle_sprites: pygame.sprite.Group, clock: pygame.time.Clock, config: Config, animations: dict[str, list[pygame.Surface]], image: pygame.Surface):
        super().__init__(position, 0.15, 6, image, (0, -26), animations, obstacle_sprites, groups)
        self.config = config
        self.clock = clock
        self.visible_sprites = groups
        self.image = image
        self.player_info = PlayerInfo(weapon=None, spell=None, weapon_data=Utilities.import_weapon_data(), spell_data=Utilities.import_magic_data())

    def input(self) -> None:
        if self.player_info.is_attacking:
            return
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = AnimationType.UP
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = AnimationType.DOWN
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = AnimationType.RIGHT
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = AnimationType.LEFT
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

    def animate(self) -> None:
        animation = self.animations[str(self.status)]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image: pygame.surface.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)


    def attack(self):
        data = self.player_info.weapon_data[self.player_info.weapon_index]
        self.player_info.weapon = Weapon(self.rect, data['type'], data['surfaces'], data['name'], data['cooldown'], data['damage'], str(self.status).split('_')[0], data['audio'], self.visible_sprites)

    def shoot(self):
        data = self.player_info.spell_data[self.player_info.spell_index]
        self.player_info.spell = Spell(self.rect, self.config, self.clock, data.spell_type, data.spell_image, data.audio, data.particles, data.name, data.strength, data.cost, str(self.status).split('_')[0], self.visible_sprites)

    def update(self) -> None:
        self.input()
        self.reset_is_attacking()
        self.reset_is_cycling()
        self.set_status()
        self.move()


    def set_status(self) -> None:

        match (self.player_info.is_attacking, self.direction.x, self.direction.y, self.status):
            case (False, 0, 0, AnimationType.LEFT):
                self.status = AnimationType.LEFT_IDLE
            case (False, 0, 0, AnimationType.UP):
                self.status = AnimationType.UP_IDLE
            case (False, 0, 0, AnimationType.RIGHT):
                self.status = AnimationType.RIGHT_IDLE
            case (False, 0, 0, AnimationType.DOWN):
                self.status = AnimationType.DOWN_IDLE
            case (True, -1, 0, AnimationType.LEFT) if AnimationType.LEFT == self.status:
                self.status = AnimationType.LEFT_ATTACK
            case (True, 0, -1, AnimationType.UP) if AnimationType.UP == self.status:
                self.status = AnimationType.UP_ATTACK
            case (True, 1, 0, AnimationType.RIGHT) if AnimationType.RIGHT == self.status:
                self.status = AnimationType.RIGHT_ATTACK
            case (True, 0, 1, AnimationType.DOWN) if AnimationType.DOWN == self.status:
                self.status = AnimationType.DOWN_ATTACK
            case (True, _, _, AnimationType.LEFT_IDLE) if AnimationType.LEFT_IDLE == self.status:
                self.status = AnimationType.LEFT_ATTACK
            case (True, _, _, AnimationType.UP_IDLE) if AnimationType.UP_IDLE == self.status:
                self.status = AnimationType.UP_ATTACK
            case (True, _, _, AnimationType.RIGHT_IDLE) if AnimationType.RIGHT_IDLE == self.status:
                self.status = AnimationType.RIGHT_ATTACK
            case (True, _, _, AnimationType.DOWN_IDLE) if AnimationType.DOWN_IDLE == self.status:
                self.status = AnimationType.DOWN_ATTACK
            case (False, _, _, AnimationType.LEFT_ATTACK):
                self.status = AnimationType.LEFT_IDLE
            case (False, _, _, AnimationType.UP_ATTACK):
                self.status = AnimationType.UP_IDLE
            case (False, _, _, AnimationType.RIGHT_ATTACK):
                self.status = AnimationType.RIGHT_IDLE
            case (False, _, _, AnimationType.DOWN_ATTACK):
                self.status = AnimationType.DOWN_IDLE

        if self.player_info.is_attacking:
            self.direction.x = 0
            self.direction.y = 0


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

@dataclass
class PlayerInfo:
    weapon_data: list[dict]
    spell_data: list[SpellInfo]
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
