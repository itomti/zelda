import pygame
import sys
import logging
import logging.config
import json
from zelda.sprite.level import Level
from zelda.config import Config
from zelda.ui.ui import UserInterface

class Game:
    def __init__(self):
        self.config = Config.make()
        pygame.init()
        self.screen = pygame.display.set_mode((self.config.user_interface.width, self.config.user_interface.height))
        pygame.display.set_caption("Zelda")
        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.get_surface()
        self.user_interface = UserInterface(self.display_surface, self.config)
        self.level = Level(self.config, self.user_interface, self.display_surface, self.clock)

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
            self.clock.tick()

def main():
    setup_logger()
    game = Game()
    game.run()

def setup_logger():
    with open("logger.json", "r") as f:
        logging.config.dictConfig(json.load(f))

if __name__ == '__main__':
    main()
