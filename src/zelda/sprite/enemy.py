import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, name: str, health: int, experience: int, damage: int, attack_type: str, attack_sound: pygame.mixer.Sound, sprites):
        super().__init__(sprites)
        self.name = name
        self.health = health
        self.experience = experience
        self.damage = damage
        self.attack_type = attack_type
        self.attack_sound = attack_sound
