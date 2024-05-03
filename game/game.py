import pygame
import sys
from game.settings import *
from game.sprite.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Zelda")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
