import pygame
import sys
import logging
import logging.config
import json
from zelda.settings import WIDTH, HEIGTH, FPS
from zelda.sprite.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Zelda")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        logging.info("starting game loop")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

def main():
    setup_logger()
    game = Game()
    game.run()

def setup_logger():
    with open("logger.json", "r") as f:
        logging.config.dictConfig(json.load(f))

if __name__ == '__main__':
    main()
