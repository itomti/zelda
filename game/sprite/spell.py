import pygame

class Spell(pygame.sprite.Sprite):
    def __init__(self, groups, spell_data: dict):
        super().__init__(groups)
        self.spell_data = spell_data
        self.name = self.spell_data['name']
        self.strength = self.spell_data['strength']
        self.cost = self.spell_data['cost']
        self.image = None
        self.rect = None

    def create(self, player_rect: pygame.rect.Rect, direction: str):
        self.image: pygame.surface.Surface = self.spell_data['graphic']
        if direction == 'right':
            self.rect: pygame.rect.Rect = self.image.get_rect(midleft=player_rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect: pygame.rect.Rect = self.image.get_rect(midright=player_rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect: pygame.rect.Rect = self.image.get_rect(midtop=player_rect.midbottom + pygame.math.Vector2(16, 0))
        elif direction == 'up':
            self.rect: pygame.rect.Rect = self.image.get_rect(midbottom=player_rect.midtop + pygame.math.Vector2(16, 0))
        else:
            self.rect: pygame.rect.Rect = self.image.get_rect(center=player_rect.center)

    def destroy(self):
        self.kill()