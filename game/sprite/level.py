import pygame

import game.utils
from game.settings import *
from game.sprite.tile import Tile
from game.sprite.player import Player
from game.sprite.camera import YSortCameraGroup
from game.sprite.weapon import Weapon
from game.ui import UserInterface
from random import choice

class Level:
    def __init__(self):
        self.player = None
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.weapon_data = import_weapon_data()
        self.create_map()
        self.ui = UserInterface()

    def run(self):
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player.rect)

    def create_map(self):
        layouts = {
            'boundary': game.utils.Utilities.import_csv_layout('assets/map/map_FloorBlocks.csv'),
            'grass': game.utils.Utilities.import_csv_layout('assets/map/map_Grass.csv'),
            'object': game.utils.Utilities.import_csv_layout('assets/map/map_Objects.csv')
        }
        graphics = {
            'grass': game.utils.Utilities.import_folder('assets/graphics/grass'),
            'objects': game.utils.Utilities.import_folder('assets/graphics/objects')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column == '-1':
                        continue
                    x = column_index * TILESIZE
                    y = row_index * TILESIZE
                    if style == 'boundary':
                        Tile((x, y), [self.obstacle_sprites], 'invisible')
                    elif style == 'grass':
                        random_grass_image = choice(graphics['grass'])
                        Tile((x, y), [self.visible_sprites], 'grass', random_grass_image)
                    elif style == 'object':
                        object_surface = graphics['objects'][int(column)]
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surface)

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites, None)