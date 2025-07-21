import pygame

from zelda.utils import Utilities
from zelda.sprite.tile import Tile
from zelda.sprite.player import Player
from zelda.sprite.camera import YSortCameraGroup
from zelda.config import Config
from zelda.ui.ui import UserInterface
from random import choice

class Level:
    def __init__(self, config: Config, ui: UserInterface, display_surface: pygame.Surface, clock: pygame.time.Clock):
        self.clock: pygame.time.Clock = clock
        self.config = config
        self.player: Player | None = None
        self.display_surface = display_surface
        self.visible_sprites: pygame.sprite.Group = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.weapon_data = Utilities.import_weapon_data()
        self.magic_data = Utilities.import_magic_data()
        self.create_map()
        self.ui = ui

    def run(self):
        self.visible_sprites.draw(self.player.rect)
        self.visible_sprites.update()
        self.ui.display(self.player)

    def create_map(self):
        layouts = {
            'boundary': Utilities.import_csv_layout('assets/map/map_FloorBlocks.csv'),
            'grass': Utilities.import_csv_layout('assets/map/map_Grass.csv'),
            'object': Utilities.import_csv_layout('assets/map/map_Objects.csv')
        }

        graphics: dict[str, list[pygame.Surface]] = {
            'grass': Utilities.import_folder('assets/graphics/grass'),
            'objects': Utilities.import_folder('assets/graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column == '-1':
                        continue
                    x = column_index * self.config.tile_size
                    y = row_index * self.config.tile_size
                    if style == 'boundary':
                        Tile(self.config, (x, y), [self.obstacle_sprites], 'invisible', None)
                    elif style == 'grass':
                        random_grass_image = choice(graphics['grass'])
                        Tile(self.config, (x, y), [self.visible_sprites], 'grass', random_grass_image)
                    elif style == 'object':
                        object_surface = graphics['objects'][int(column)]
                        Tile(self.config, (x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surface)

        animations = Utilities.import_player_assets()
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, self.clock, self.config, animations)
