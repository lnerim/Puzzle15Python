from copy import deepcopy
from datetime import datetime
from random import choice

import pygame
from pygame import Surface, Rect
from pygame.sprite import Sprite, Group

from variables import Colors, PLACE_SIZE, Coordinates, INIT_MATRIX, FONT, SURFACE_LOCATE, IND, GameStatus, START_PER, \
    OFFSET_PER, DICE_PER, SWAP_COUNT


class Dice(Sprite, Group):
    def __init__(self, number: int, *, image_path: str | None = None):
        super().__init__()

        self.number = number
        self.size = PLACE_SIZE * DICE_PER
        self.size_dice = (self.size, self.size)

        self.offset_x, self.offset_y = SURFACE_LOCATE

        self.image = pygame.Surface(self.size_dice)

        if image_path:
            img = pygame.image.load(image_path)
            img = pygame.transform.scale(img, (PLACE_SIZE, PLACE_SIZE))

            w, h = img.get_width(), img.get_height()

            # Порядковый номер в строку и столбец для фото
            image_row = (self.number - 1) % 4
            image_column = (self.number - 1) // 4

            cropped_region = (
                x := w * (START_PER + OFFSET_PER * image_row),
                y := h * (START_PER + OFFSET_PER * image_column),
                x + OFFSET_PER*w, y + OFFSET_PER*h
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


class Place:
    def __init__(self, screen: Surface, *, image_path: str | None):
        self.screen = screen
        self.surface = Surface((PLACE_SIZE, PLACE_SIZE))

        self.time0 = datetime.now()
        self.steps = 0
        self.image_path = image_path

        self.dices_group: Group[Dice] = Group()

        # Игровая матрица пятнашек
        self.matrix: list[list[int]] = deepcopy(INIT_MATRIX)
        self.zero_coord = Coordinates(3, 3)

    def game(self) -> GameStatus:
        self.generate_place()

        for i in range(4):
            for j in range(4):
                if number := self.matrix[i][j]:  # Все, кроме нуля
                    dice: Dice = Dice(number, image_path=self.image_path)

                    dice.rect.y = dice.offset_y + PLACE_SIZE * (START_PER + OFFSET_PER * i)
                    dice.rect.x = dice.offset_x + PLACE_SIZE * (START_PER + OFFSET_PER * j)

                    self.dices_group.add(dice)

        while True:
            self.draw_place()

            if pygame.event.get(pygame.QUIT):
                return GameStatus.END
            elif pygame.event.get(pygame.MOUSEBUTTONUP):
                if self.click():
                    if self.check_win():
                        return GameStatus.WIN

            self.dices_group.draw(self.screen)

            pygame.display.update()

            pygame.time.Clock().tick(100)

    def draw_place(self):
        self.screen.fill(Colors.APRICOT)

        font = pygame.font.Font(FONT, 24)

        # Время
        game_time = datetime.now() - self.time0
        time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds % 60 :02}"
        text_time = font.render(f"Время {time_str}", True, Colors.BLACKBERRY)
        self.screen.blit(text_time, (IND, IND))

        # Ходов
        text_steps = font.render(f"Ходов {self.steps}", True, Colors.BLACKBERRY)
        locate_steps = (self.screen.get_width() - text_steps.get_width() - IND, IND)
        self.screen.blit(text_steps, locate_steps)

        # Игровое поле
        self.surface.fill(Colors.LIGHT_CORAL)
        self.screen.blit(self.surface, SURFACE_LOCATE)

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
        for i in range(SWAP_COUNT):
            select: Coordinates = choice(self.movable_dice())
            self.change_dice(select)

    def change_dice(self, select: Coordinates):
        s_row, s_column = select.row, select.column
        z_row, z_column = self.zero_coord.row, self.zero_coord.column

        self.matrix[z_row][z_column], self.matrix[s_row][s_column] = (
            self.matrix[s_row][s_column], self.matrix[z_row][z_column])

        self.zero_coord = Coordinates(s_row, s_column)

    def click(self) -> bool:  # Удачный или нет клик
        pos = pygame.mouse.get_pos()
        for elem in self.movable_dice():
            for dice in self.dices_group:
                if dice.number == self.matrix[elem.row][elem.column]:
                    if dice.rect.collidepoint(pos):
                        pygame.mixer.Sound("dice.mp3").play()
                        self.anim_move(dice, self.zero_coord)

                        self.change_dice(elem)
                        self.steps += 1

                        return True
        return False

    def anim_move(self, dice: Dice, elem: Coordinates):
        # Конечные координаты
        pos_y = dice.offset_y + PLACE_SIZE * (START_PER + OFFSET_PER * elem.row)
        pos_x = dice.offset_x + PLACE_SIZE * (START_PER + OFFSET_PER * elem.column)

        h = 5  # Шаг анимации

        # Шаг для каждого направления
        h_y = (pos_y - dice.rect.y) / h
        h_x = (pos_x - dice.rect.x) / h

        for _ in range(h):
            # temp - закрашивает предыдущее положение
            temp = pygame.Surface(dice.size_dice)
            temp.fill(Colors.LIGHT_CORAL)

            temp.get_rect().y = dice.rect.y
            temp.get_rect().x = dice.rect.x

            self.screen.blit(temp, (dice.rect.x, dice.rect.y))

            dice.rect.move_ip(h_x, h_y)

            self.dices_group.draw(self.screen)
            pygame.display.update()
            pygame.time.Clock().tick(100)

        dice.rect.x = pos_x
        dice.rect.y = pos_y

    def check_win(self) -> bool:
        return INIT_MATRIX == self.matrix

    def get_record(self) -> tuple[datetime, int]:
        return self.time0, self.steps
