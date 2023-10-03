from dataclasses import dataclass

NAME = "Пятнашки"

WIDTH = 700
HEIGHT = 740


PLACE_SIZE = min(WIDTH, HEIGHT) - 20


@dataclass
class GameStatus:
    MENU = "menu"
    START = "start"
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
