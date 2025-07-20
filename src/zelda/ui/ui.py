from __future__ import annotations
import pygame
from zelda.sprite.player import Player
from zelda.config import Config

class UserInterface:
    def __init__(self, display_surface, config: Config):
        # general info
        self.ui_settings = config.user_interface
        self.display_surface: pygame.surface.Surface = display_surface
        self.font = pygame.font.Font(self.ui_settings.font.path, self.ui_settings.font.size)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, self.ui_settings.healthBar.width, self.ui_settings.healthBar.height)
        self.energy_bar_rect = pygame.Rect(10, 34, self.ui_settings.energyBar.width, self.ui_settings.energyBar.height)

    def show_bar(self, current_amount, max_amount, background_rect, color) -> None:
        # draw background
        pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.background, background_rect)

        # convert stat to px
        ratio = current_amount / max_amount
        current_width = background_rect.width * ratio
        current_rect: pygame.rect.Rect = background_rect.copy()
        current_rect.width = current_width
        # drawing the bar!
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.background, background_rect, 3)

    def show_experience(self, experience: str) -> None:
        text_surface = self.font.render(experience, False, self.ui_settings.ui_color.text)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surface.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.background, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.border, text_rect.inflate(10, 10), 3)

    def selection_box(self, left, top, player: Player) -> pygame.rect.Rect:
        bg_rect = pygame.Rect(left, top, self.ui_settings.item_box_size, self.ui_settings.item_box_size)
        pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.background, bg_rect)
        if player.is_cycling:
            pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.active, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, self.ui_settings.ui_color.border, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, player: Player) -> None:
        bg_rect = self.selection_box(10, 600, player)
        weapon_surface: pygame.surface.Surface = player.weapon_data[player.weapon_index].direction_surfaces['full']
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, player: Player) -> None:
        bg_rect = self.selection_box(80, 635, player)
        spell_surface: pygame.surface.Surface = player.spell_data[player.spell_index].direction_surfaces['graphic']
        spell_rect = spell_surface.get_rect(center=bg_rect.center)
        self.display_surface.blit(spell_surface, spell_rect)

    def display(self, player: Player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, self.ui_settings.healthBar.color)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, self.ui_settings.energyBar.color)
        self.show_experience(str(int(player.experience)))
        self.weapon_overlay(player)
        self.magic_overlay(player)
