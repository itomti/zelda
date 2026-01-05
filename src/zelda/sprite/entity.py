import pygame
import logging
from zelda.direction import DirectionType

class Entity(pygame.sprite.Sprite):
    def __init__(self, position, animation_speed: float, speed: float, image: pygame.Surface, hit_box: tuple, animations: dict[str, list[pygame.Surface]], obstacles: pygame.sprite.Group, groups: pygame.sprite.Group):
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
