from dataclasses import dataclass
from enum import Enum

import pygame
from pygame import Surface
from pygame.font import Font
from pygame.sprite import Sprite

from variables import FONT, Colors


@dataclass
class ButtonColor:
    text: tuple[int, int, int]
    background: tuple[int, int, int]


class ButtonState(Enum):
    PRESS = "press"
    ACTIVE = "active"
    INACTIVE = "inactive"
    HOVER = "hover"


@dataclass
class ButtonPalette:
    PRESS: ButtonColor
    ACTIVE: ButtonColor
    INACTIVE: ButtonColor
    HOVER: ButtonColor

    def __getitem__(self, state: ButtonState) -> ButtonColor:
        match state:
            case ButtonState.ACTIVE:
                return self.ACTIVE
            case ButtonState.PRESS:
                return self.PRESS
            case ButtonState.INACTIVE:
                return self.INACTIVE
            case ButtonState.HOVER:
                return self.HOVER


class Button(Sprite):
    def __init__(self,
                 text: str,
                 on_click: callable,
                 size: tuple[int, int],
                 pos: tuple[int, int],
                 palette: ButtonPalette,
                 text_size: int | float
                 ):
        super().__init__()

        self.text = text
        self.on_click = on_click
        self.size = size
        self.palette: ButtonPalette = palette
        self.text_size = text_size

        self._state: ButtonState = ButtonState.ACTIVE
        self.color: ButtonColor = self.palette[self._state]
        self.text_color = self.color.text
        self.background_color = self.color.background

        self.image = Surface(self.size)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: ButtonState):
        self._state = value
        self.color = self.palette[value]

    def draw(self):
        self.image.fill(self.color.background)
        font = Font(FONT, self.text_size)

        text_button = font.render(self.text, True, Colors.BLACKBERRY)
        text_button_x = self.size[0] / 2 - text_button.get_width() / 2
        text_button_y = self.size[1] / 2 - text_button.get_height() / 2
        self.image.blit(text_button, (text_button_x, text_button_y))

    def update(self):
        if self.state == ButtonState.INACTIVE:
            self.draw()
            return

        pos = pygame.mouse.get_pos()
        if not self.rect.collidepoint(pos):
            self.state = ButtonState.ACTIVE
            self.draw()
            return

        is_pressed = pygame.mouse.get_pressed()[0]  # Левая кнопка мыши
        if not is_pressed and self.state == ButtonState.PRESS:
            self.on_click()
            self.state = ButtonState.ACTIVE
        elif is_pressed:
            self.state = ButtonState.PRESS
        else:
            self.state = ButtonState.HOVER

        self.draw()
