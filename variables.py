from dataclasses import dataclass

FONT = r"Zametka Parletter.ttf"

NAME = "Пятнашки"

WIDTH = 700
HEIGHT = 740

PLACE_SIZE = min(WIDTH, HEIGHT) * 0.99

# Решение и начальная позиция пятнашек
INIT_MATRIX: list[list[int]] = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9,  10, 11, 12],
    [13, 14, 15, 0],
]


@dataclass
class GameStatus:
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
