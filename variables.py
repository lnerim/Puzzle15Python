from dataclasses import dataclass
from enum import Enum

FONT = r"Zametka Parletter.ttf"

NAME = "Пятнашки"

PATH_IMAGES = "images"
PATH_RECORD = "record.txt"

SWAP_COUNT = 100

WIDTH = 700
HEIGHT = 740

PLACE_SIZE = min(WIDTH, HEIGHT) * 0.985  # Процентов от изначального

DICE_PER = 0.24  # Размер кости в процентах
OFFSET_PER = 0.25  # Размер кости и отступа в процентах
START_PER = 0.005  # Размер начального отступа в процентах

IND = 5  # indention - отступ для текста

# Расположение Surface с костями
SURFACE_LOCATE = (
    WIDTH / 2 - PLACE_SIZE / 2,
    (HEIGHT + 24 + IND) / 2 - PLACE_SIZE / 2  # Где 24 - размер высоты шрифта времени
)

# Решение и начальная позиция пятнашек
INIT_MATRIX: list[list[int]] = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9,  10, 11, 12],
    [13, 14, 15, 0],
]


class GameStatus(Enum):
    MENU = "menu"
    GAME = "game"
    WIN = "win"
    END = "end"


@dataclass
class Colors:
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    DARK_PURPLE = (148, 0, 211)
    FOREST_WOLF = (219, 215, 210)

    APRICOT = (255, 205, 178)
    LIGHT_CORAL = (255, 180, 162)
    PINK_PURPLE = (229, 152, 155)
    PINK_PURPLE_DARK = (222, 145, 148)
    PINK_PURPLE_BLACK = (159, 82, 85)
    DULL_PURPLE = (181, 131, 141)
    BLACKBERRY = (85, 81, 91)


@dataclass
class Coordinates:
    row: int
    column: int

    def up(self):
        row = self.row - 1
        column = self.column
        return Coordinates(row, column)

    def down(self):
        row = self.row + 1
        column = self.column
        return Coordinates(row, column)

    def left(self):
        row = self.row
        column = self.column - 1
        return Coordinates(row, column)

    def right(self):
        row = self.row
        column = self.column + 1
        return Coordinates(row, column)


class GameMode(Enum):
    NORMAL = "normal"
    IMAGE = "image"
