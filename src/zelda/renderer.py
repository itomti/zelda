import pygame
from zelda.ui.ui import UserInterface


class Renderer(pygame.sprite.Group):
    def __init__(self, ui: UserInterface, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.groups = groups
        self.obstacles = pygame.sprite.Group()
        self.ui = ui

    def render(self):
        self.groups.update()
