import pygame
import os
import json
import logging
from csv import reader
from zelda.sprite.weapon import Weapon
from zelda.sprite.spell import SpellType, SpellInfo

class Utilities:
    @staticmethod
    def import_csv_layout(path) -> list[list[str]]:
        terrain_map: list[list[str]] = []
        with open(path) as file:
            layout = reader(file, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
        return terrain_map

    @staticmethod
    def import_folder(path) -> list[pygame.Surface]:
        if not os.path.exists(path):
            return []
        surfaces: list[pygame.Surface] = []
        for _, __, image_files in os.walk(path):
            for image in image_files:
                full_path = f"{path}/{image}"
                surface: pygame.Surface = pygame.image.load(full_path).convert_alpha()
                surfaces.append(surface)
        return surfaces

    @staticmethod
    def import_player_assets() -> dict[str, list[pygame.Surface]]:
        character_path = 'assets/graphics/player'
        animations = {
            'left': [],
            'left_attack': [],
            'left_idle': [],
            'up': [],
            'up_attack': [],
            'up_idle': [],
            'right': [],
            'right_attack': [],
            'right_idle': [],
            'down': [],
            'down_attack': [],
            'down_idle': []
        }

        for animation in animations.keys():
            folder_path: str = f"{character_path}/{animation}"
            surfaces = Utilities.import_folder(folder_path)
            animations[animation] = surfaces

        return animations

    @staticmethod
    def import_weapon_data() -> list[dict]:
        weapons: list[dict] = [
            Weapon.create_axe(),
            Weapon.create_lance(),
            Weapon.create_rapier(),
            Weapon.create_sai(),
            Weapon.create_sword()
        ]
        return weapons


    @staticmethod
    def import_magic_data() -> list[SpellInfo]:
        magic: list[SpellInfo] = []
        spell_img: pygame.Surface = pygame.image.load('assets/graphics/particles/flame/fire.png').convert_alpha()
        particles: list[pygame.Surface] = Utilities.import_folder('assets/graphics/particles/flame/frames')
        audio = pygame.mixer.Sound("assets/audio/Fire.wav")
        spell = SpellInfo('flame', SpellType.FLAME, 20, 10, spell_img, particles, audio, 0.15)

        magic.append(spell)

        spell_img: pygame.Surface = pygame.image.load('assets/graphics/particles/heal/heal.png').convert_alpha()
        particles: list[pygame.Surface] = Utilities.import_folder('assets/graphics/particles/heal/frames')

        audio = pygame.mixer.Sound("assets/audio/heal.wav")
        spell = SpellInfo('heal', SpellType.HEAL, 5, 10, spell_img, particles, audio, 0.15)

        magic.append(spell)

        return magic

    @staticmethod
    def import_monster_data(path: str) -> dict[str, dict]:
        if not os.path.exists(path):
            return {}
        monsters: dict[str, dict] = {}
        for _, dirs, _ in os.walk(path):
            for dirname in dirs:
                for _, _, files in os.walk(f"{path}/{dirname}"):
                    for fi in files:
                        if "settings.json" not in fi:
                            continue
                        with open(f"{path}/{dirname}/{fi}", "r") as f:
                            monster: dict = json.load(f)
                            monster['image'] = pygame.image.load(monster['image']).convert_alpha()
                            monsters[monster['name']] = monster

        return monsters
