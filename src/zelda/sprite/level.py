import os
import pathlib
import logging
import pygame
import random
from zelda.utils import Utilities
from zelda.sprite.tile import Tile
from zelda.sprite.player import Player, PlayerInfo
from zelda.sprite.camera import YSortCameraGroup
from zelda.sprite.spell import SpellInfo
from zelda.sprite.enemy import Enemy, EnemyInfo
from zelda.config import Config
from zelda.ui.ui import UserInterface
from random import choice

class Level:
    def __init__(self, config: Config, ui: UserInterface, display_surface: pygame.Surface, clock: pygame.time.Clock):
        self.clock: pygame.time.Clock = clock
        self.config = config
        self.player: Player
        self.display_surface = display_surface
        self.visible_sprites: YSortCameraGroup = YSortCameraGroup(pygame.sprite.Group())
        self.obstacle_sprites = pygame.sprite.Group()
        self.monsters: list[Enemy] = []
        self.create_map()
        self.create_player()
        self.create_monsters()
        self.ui = ui
        self.moving_monsters: list[Enemy] = []

    def run(self):
        self.visible_sprites.draw(self.player.rect)
        self.visible_sprites.update()
        self.ui.display(self.player)
        self.move_monsters_random()

    def move_monsters_random(self) -> None:
        if len(self.moving_monsters) == 0:
            self.pick_monsters_to_move()

        for monster in self.moving_monsters:
            monster.random_move()

        for monster in self.moving_monsters:
            if monster.can_move:
                self.moving_monsters.remove(monster)

    def pick_monsters_to_move(self) -> None:
        movable = [m for m in self.monsters if m.can_move == True]
        if len(movable) == 0:
            return

        for _ in range(2):
            m = self.monsters[random.randint(0, len(movable) - 1)]
            if not m.can_move:
                continue

            self.moving_monsters.append(m)

    def create_map(self):
        layouts = {
            'boundary': Utilities.import_csv_layout('assets/map/map_FloorBlocks.csv'),
            'grass': Utilities.import_csv_layout('assets/map/map_Grass.csv'),
            'object': Utilities.import_csv_layout('assets/map/map_Objects.csv')
        }

        graphics: dict[str, list[pygame.Surface]] = {
            'grass': Utilities.import_folder(pathlib.Path('assets/graphics/grass')),
            'objects': Utilities.import_folder(pathlib.Path('assets/graphics/objects'))
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

    def create_monsters(self):
        monster_data = Utilities.import_monster_data('assets/monsters')
        for monster in monster_data.keys():
            m = monster_data[monster]
            logging.info(f"creating {m['name']}")
            enemy_info = EnemyInfo(m['name'], m['health'], m['experience'], m['damage'], m['attack_type'], m['attack_type'], m['image'], m['animations'])
            randx = random.randint(1900, 2000)
            randy = random.randint(1300, 1500)
            enemy = Enemy((randx, randy), enemy_info, self.obstacle_sprites, self.visible_sprites)
            self.monsters.append(enemy)

    def create_player(self):
        player_animations = Utilities.import_player_animations()
        image = pygame.image.load("assets/graphics/player/down/down_0.png").convert_alpha()
        player_info = PlayerInfo(weapon=None, spell=None, weapon_data=Utilities.import_weapon_data(), spell_data=Utilities.import_magic_data(), animations=player_animations)
        self.player = Player(player_info, (2000, 1430), self.visible_sprites, self.obstacle_sprites, self.clock, self.config, image)
