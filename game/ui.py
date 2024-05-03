import pygame
from game.settings import *


class UserInterface:
    def __init__(self):
        # general info
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/font/joystix.ttf')

    def display(self, player_rect):
        pass
