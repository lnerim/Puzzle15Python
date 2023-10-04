from dataclasses import dataclass

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
