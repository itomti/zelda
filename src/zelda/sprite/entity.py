from enum import IntEnum
import pygame
import logging
from zelda.direction import DirectionType

class AnimationType(IntEnum):
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

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, animation_speed: float, speed: float, image: pygame.Surface, hit_box: tuple, animations: dict[str, list[pygame.Surface]], status: AnimationType, obstacles: pygame.sprite.Group, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.hit_box = self.rect.inflate(hit_box)
        self.obstacles = obstacles
        self.frame_index: float = 0
        self.animations: dict[str, list[pygame.Surface]] = animations
        self.animation_speed: float = animation_speed
        self.speed = speed
        self.direction = pygame.math.Vector2()
        self.status = status

    def animate(self) -> None:
        animation = self.animations[str(self.status)]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image: pygame.surface.Surface = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def collision(self, direction: DirectionType):
        if direction == DirectionType.HORIZONTAL:
            for sprite in self.obstacles:
                if sprite.hit_box.colliderect(self.hit_box):
                    if self.direction.x > 0:
                        self.hit_box.right = sprite.hit_box.left
                    elif self.direction.x < 0:
                        self.hit_box.left = sprite.hit_box.right

        if direction == DirectionType.VERTICAL:
            for sprite in self.obstacles:
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


class MagicEntity(Entity):
    def __init__(self):
        self.spell_index = 0
        self.spell_data: list[dict]
