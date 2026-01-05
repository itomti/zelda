from asyncio.queues import Queue
from asyncio.events import AbstractEventLoop
import pygame
import sys
import logging
import logging.config
import json
import asyncio
import time
from zelda.sprite.level import Level
from zelda.config import Config
from zelda.ui.ui import UserInterface

class Game:
    def __init__(self, loop: AbstractEventLoop, event_queue: Queue):
        pygame.init()
        self.loop = loop
        self.event_queue = event_queue
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.display_surface = pygame.display.get_surface()
        self.audio: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/main.ogg")
        self.config = Config.make()
        self.screen = pygame.display.set_mode((self.config.user_interface.width, self.config.user_interface.height))
        self.user_interface = UserInterface(self.display_surface, self.config)
        self.level = Level(self.config, self.user_interface, self.display_surface, self.clock)
        self.audio.set_volume(0.25)
        self.audio.play(0, 0, 100)
        pygame.display.set_caption("Zelda")
        
    
    def pygame_event_loop(self):
        while True:
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(self.event_queue.put(event), loop=self.loop)
            

    async def update(self):
        current_time = 0
        while True:
            last_time, current_time = current_time, time.time()
            """
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.audio.stop()
                    pygame.quit()
                    sys.exit()            
            """
            
            self.screen.fill('black')
            
            pygame.display.update()
            #await asyncio.sleep(1 / self.config.fps)
            #await asyncio.sleep(min(1 / self.config.fps - (current_time - last_time - 1 / self.config.fps), 1 / self.config.fps))  # tick
            


    async def handle_events(self):
        while True:            
            event = await self.event_queue.get()
            if event.type == pygame.QUIT:
                self.audio.stop()
                pygame.quit()
                sys.exit()

            self.level.run()
            logging.info("running")

    def run(self):
        asyncio.ensure_future(self.handle_events())
        asyncio.ensure_future(self.update())
        
        
        #asyncio.ensure_future(self.init_game())


def main():
    setup_logger()
    loop = asyncio.get_event_loop()
    event_queue = asyncio.Queue()
    game = Game(loop, event_queue)
    game.run()
    loop.run_in_executor(None, game.pygame_event_loop)
    loop.run_forever()

    #asyncio.run(game.run())
    

def setup_logger():
    with open("logger.json", "r") as f:
        logging.config.dictConfig(json.load(f))

if __name__ == '__main__':
    main()
