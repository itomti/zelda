import pygame
import os
from csv import reader

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
