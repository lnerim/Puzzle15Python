from copy import deepcopy
from datetime import datetime
from random import choice

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from variables import Colors, PLACE_SIZE, Coordinates, INIT_MATRIX, FONT


class Dice(Sprite):
    def __init__(self, number: int,
                 row: int, column: int,
                 offset_x: float | int, offset_y: float | int,
                 image_path: str | None = r"images/i.webp" and None):
        super().__init__()

        self.number = number
        self.size = PLACE_SIZE * 0.24
        self.size_dice = (self.size, self.size)

        self.row = row
        self.column = column

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.image = pygame.Surface(self.size_dice)

        if image_path:
            img = pygame.image.load(image_path)

            w, h = img.get_width(), img.get_height()

            image_row = (self.number - 1) % 4
            image_column = (self.number - 1) // 4

            cropped_region = (
                x := self.offset_x + w * (0.005 + 0.25 * image_row),
                y := self.offset_y + h * (0.005 + 0.25 * image_column),
                x+0.25*w, y+0.25*h
            )

            self.image.blit(img, (0, 0), cropped_region)

        else:
            self.image.fill(Colors.PINK_PURPLE)
            font = pygame.font.Font(FONT, 72)

            text_number = font.render(str(number), True, Colors.BLACKBERRY)
            text_number_w = text_number.get_width() / 2
            text_number_h = text_number.get_height() / 2
            self.image.blit(text_number, (self.size / 2 - text_number_w, self.size / 2 - text_number_h))

        self.rect: Rect = self.image.get_rect()
        self.rect.y = self.offset_y + PLACE_SIZE * (0.005 + 0.25 * self.row)
        self.rect.x = self.offset_x + PLACE_SIZE * (0.005 + 0.25 * self.column)


class Place:
    def __init__(self, screen: Surface):
        self.screen = screen
        self.surface = Surface((PLACE_SIZE, PLACE_SIZE))

        self.time0 = datetime.now()
        self.steps = 0

        self.dices_group: Group[Dice] = Group()

        # Игровая матрица пятнашек
        self.matrix: list[list[int]] = deepcopy(INIT_MATRIX)
        self.zero_coord = Coordinates(3, 3)

    def draw(self):
        self.screen.fill(Colors.APRICOT)

        ind = 5  # indention - отступ для текста

        font = pygame.font.Font(FONT, 24)

        # Время
        game_time = datetime.now() - self.time0
        time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds % 60 :02}"
        text_time = font.render(f"Время {time_str}", True, Colors.BLACKBERRY)
        self.screen.blit(text_time, (ind, ind))

        # Ходов
        text_steps = font.render(f"Ходов {self.steps}", True, Colors.BLACKBERRY)
        locate_steps = (self.screen.get_width() - text_steps.get_width() - ind, ind)
        self.screen.blit(text_steps, locate_steps)

        # Игровое поле
        self.surface.fill(Colors.LIGHT_CORAL)
        surface_locate = (
            self.screen.get_width() / 2 - PLACE_SIZE / 2,
            (self.screen.get_height() + text_time.get_height() + ind) / 2 - PLACE_SIZE / 2,
        )
        self.screen.blit(self.surface, surface_locate)

        dices = []
        for i in range(4):
            for j in range(4):
                if number := self.matrix[i][j]:
                    dice: Sprite = Dice(number, i, j, *surface_locate)
                    dices.append(dice)

        self.dices_group = Group(*dices)
        self.dices_group.draw(self.screen)

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

    def click(self):
        pos = pygame.mouse.get_pos()
        for elem in self.movable_dice():
            dice: Dice
            for dice in self.dices_group:
                if (dice.row == elem.row) and (dice.column == elem.column):
                    if dice.rect.collidepoint(pos):
                        pygame.mixer.Sound("dice.mp3").play()
                        self.anim_move(dice, self.zero_coord)

                        self.change_dice(elem)
                        self.steps += 1
                        break

    def anim_move(self, dice: Dice, elem: Coordinates):
        pos_y = dice.offset_y + PLACE_SIZE * (0.005 + 0.25 * elem.row)
        pos_x = dice.offset_x + PLACE_SIZE * (0.005 + 0.25 * elem.column)

        h = 5

        h_y = (pos_y - dice.rect.y) / h
        h_x = (pos_x - dice.rect.x) / h

        for _ in range(h):
            temp = pygame.Surface(dice.size_dice)
            temp.fill(Colors.LIGHT_CORAL)

            temp.get_rect().y = dice.rect.y
            temp.get_rect().x = dice.rect.x

            self.screen.blit(temp, (dice.rect.x, dice.rect.y))

            dice.rect.move_ip(h_x, h_y)

            self.dices_group.draw(self.screen)
            pygame.display.update()
            pygame.time.Clock().tick(100)

    def check_win(self) -> bool:
        return INIT_MATRIX == self.matrix

    def get_record(self) -> tuple[datetime, int]:
        return self.time0, self.steps
