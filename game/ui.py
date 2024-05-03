import pygame
from game.sprite.player import Player

class UserInterfaceSettings:
    def __init__(self, font_path, font_size, bar_height, health_bar_width, energy_bar_width, health_color,
                 energy_color, background_color, water_color, border_color, text_color, item_box_size):
        self.font_path = font_path
        self.font_size = font_size
        self.bar_height = bar_height
        self.health_bar_width = health_bar_width
        self.energy_bar_width = energy_bar_width
        self.health_color = health_color
        self.energy_color = energy_color
        self.background_color = background_color
        self.water_color = water_color
        self.border_color = border_color
        self.text_color = text_color
        self.item_box_size = item_box_size

class UserInterface:
    def __init__(self, display_surface, ui_settings: UserInterfaceSettings):
        # general info
        self.ui_settings = ui_settings
        self.display_surface: pygame.surface.Surface = display_surface
        self.font = pygame.font.Font(ui_settings.font_path, ui_settings.font_size)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, self.ui_settings.health_bar_width, self.ui_settings.bar_height)
        self.energy_bar_rect = pygame.Rect(10, 34, self.ui_settings.energy_bar_width, self.ui_settings.bar_height)

    def show_bar(self, current_amount, max_amount, background_rect, color) -> None:
        # draw background
        pygame.draw.rect(self.display_surface, self.ui_settings.background_color, background_rect)

        # convert stat to px
        ratio = current_amount / max_amount
        current_width = background_rect.width * ratio
        current_rect: pygame.rect.Rect = background_rect.copy()
        current_rect.width = current_width
        # drawing the bar!
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, self.ui_settings.background_color, background_rect, 3)

    def show_experience(self, experience: str) -> None:
        text_surface = self.font.render(experience, False, self.ui_settings.text_color)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, self.ui_settings.background_color, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, self.ui_settings.border_color, text_rect.inflate(10, 10), 3)

    def selection_box(self, left, top, player: Player) -> pygame.rect.Rect:
        bg_rect = pygame.Rect(left, top, self.ui_settings.item_box_size, self.ui_settings.item_box_size)
        pygame.draw.rect(self.display_surface, self.ui_settings.background_color, bg_rect)
        pygame.draw.rect(self.display_surface, self.ui_settings.border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, player: Player) -> None:
        bg_rect = self.selection_box(10, 600, player)
        weapon_surface: pygame.surface.Surface = player.weapon_data[player.current_weapon_name]['direction_surfaces']['full']
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, player: Player) -> None:
        self.selection_box(80, 635, player)

    def display(self, player: Player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, self.ui_settings.health_color)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, self.ui_settings.energy_color)
        self.show_experience(str(int(player.experience)))
        self.weapon_overlay(player)
        self.magic_overlay(player)

