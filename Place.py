from datetime import datetime

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from variables import Colors, PLACE_SIZE


class Dice(Sprite):
    ...


class Place:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.surface = Surface((PLACE_SIZE, PLACE_SIZE))

        self.time0 = datetime.now()
        self.steps = 0

    def draw(self):
        self.screen.fill(Colors.FOREST_WOLF)

        font = pygame.font.Font(pygame.font.get_default_font(), 24)

        # Время
        game_time = datetime.now() - self.time0
        time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds :02}"
        text_time = font.render(f"Время: {time_str}", True, Colors.RED)
        self.screen.blit(text_time, (5, 5))

        # Ходов
        text_steps = font.render(f"Ходов: {self.steps}", True, Colors.RED)
        locate_steps = (self.screen.get_width() - text_steps.get_width() - 5, 5)
        self.screen.blit(text_steps, locate_steps)

        self.surface.fill(Colors.GREEN)
        surface_locate = (
            self.screen.get_width() / 2 - PLACE_SIZE / 2,
            (self.screen.get_height() + text_time.get_height()) / 2 - PLACE_SIZE / 2,
        )
        self.screen.blit(self.surface, surface_locate)
