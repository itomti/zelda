import pygame
from zelda.direction import DirectionType

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index: float = 0
        self.animation_speed: float = 0.15
        self.direction = pygame.math.Vector2()


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
