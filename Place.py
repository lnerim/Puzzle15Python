from copy import deepcopy
from datetime import datetime
from random import choice

import pygame
from pygame import Surface
from pygame.sprite import Sprite, Group

from variables import Colors, PLACE_SIZE, Coordinates, INIT_MATRIX


class Dice(Sprite):
    def __init__(self, number: int, row, column, offset_x, offset_y):
        super().__init__()
        self.number = number
        self.size = PLACE_SIZE * 0.24
        self.size_dice = (self.size, self.size)

        self.row = row
        self.column = column

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.image = pygame.Surface(self.size_dice)

        self.image.fill(Colors.BLACK)
        self.rect = self.image.get_rect()
        self.set_locate()

    def set_locate(self):
        self.rect.x = self.offset_x + PLACE_SIZE * (0.005 + 0.25 * self.row)
        self.rect.y = self.offset_y + PLACE_SIZE * (0.005 + 0.25 * self.column)

    def move_to(self, row: int, column: int):
        self.row = row
        self.column = column

        pos_x = 0.05 + 0.25 * row
        pos_y = 0.05 + 0.25 * column

        self.rect.move(pos_x, pos_y)


class Place:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.surface = Surface((PLACE_SIZE, PLACE_SIZE))

        self.time0 = datetime.now()
        self.steps = 0

        # Игровая матрица пятнашек
        self.matrix: list[list[int]] = deepcopy(INIT_MATRIX)
        self.zero_coord = Coordinates(3, 3)

    def draw(self):
        self.screen.fill(Colors.FOREST_WOLF)

        ind = 5  # indention - отступ для текста

        font = pygame.font.Font(pygame.font.get_default_font(), 24)

        # Время
        game_time = datetime.now() - self.time0
        time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds % 60 :02}"
        text_time = font.render(f"Время: {time_str}", True, Colors.RED)
        self.screen.blit(text_time, (ind, ind))

        # Ходов
        text_steps = font.render(f"Ходов: {self.steps}", True, Colors.RED)
        locate_steps = (self.screen.get_width() - text_steps.get_width() - ind, ind)
        self.screen.blit(text_steps, locate_steps)

        # Игровое поле
        self.surface.fill(Colors.GREEN)
        surface_locate = (
            self.screen.get_width() / 2 - PLACE_SIZE / 2,
            (self.screen.get_height() + text_time.get_height() + ind) / 2 - PLACE_SIZE / 2,
        )
        self.screen.blit(self.surface, surface_locate)

        dices = []
        for i in range(4):
            for j in range(4):
                dice: Sprite = Dice(i * 4 + j, i, j, *surface_locate)
                dices.append(dice)
        dices.pop()

        dices_group: Group[Dice] = Group(*dices)
        dices_group.draw(self.screen)

    def movable_dice(self) -> tuple[Coordinates]:
        movements: list[Coordinates] = list()
        coord = self.zero_coord

        if coord.row > 0:
            movements.append(coord.up())
        if coord.row < 3:
            movements.append(coord.down())
        if coord.column > 0:
            movements.append(coord.left())
        if coord.column < 3:
            movements.append(coord.right())

        return tuple(movements)

    def generate_place(self):
        for i in range(100):
            select: Coordinates = choice(self.movable_dice())
            self.change_dice(select)

    def change_dice(self, select: Coordinates):
        s_row, s_column = select.row, select.column
        z_row, z_column = self.zero_coord.row, self.zero_coord.column

        self.matrix[z_row][z_column], self.matrix[s_row][s_column] = (
            self.matrix[s_row][s_column], self.matrix[z_row][z_column])

        self.zero_coord = Coordinates(s_row, s_column)
