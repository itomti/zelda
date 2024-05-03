import pygame
import os
from csv import reader


class Utilities:
    @staticmethod
    def import_csv_layout(path):
        terrain_map = []
        with open(path) as file:
            layout = reader(file, delimiter=',')
            for row in layout:
                terrain_map.append(list(row))
        return terrain_map

    @staticmethod
    def import_folder(path):
        if not os.path.exists(path):
            return
        surfaces = []
        for _, __, image_files in os.walk(path):
            for image in image_files:
                full_path = f"{path}/{image}"
                surface = pygame.image.load(full_path).convert_alpha()
                surfaces.append(surface)

        return surfaces
