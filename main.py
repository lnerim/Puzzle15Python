from datetime import datetime, timedelta
from os import listdir
from os.path import exists
from random import shuffle

import pygame
from pygame import Surface

from Place import Place
from ui.Button import Button, ButtonGroup, ButtonState
from variables import *


class Game:
    def __init__(self):
        pygame.init()
        self.game_status = GameStatus.MENU
        self.game_mode: GameMode | None = None
        self.screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))

        self.time0 = None
        self.steps = None

        self.image = None

        self.clock = pygame.time.Clock()

        pygame.display.set_caption(NAME)

    def main_loop(self):
        while True:
            match self.game_status:
                case GameStatus.MENU:
                    self.menu()
                case GameStatus.GAME:
                    image = None
                    if self.game_mode == GameMode.IMAGE:
                        image = self.image

                    self.game(image_path=image)
                    self.game_mode = None
                    self.image = None
                case GameStatus.END:
                    self.end()
                case GameStatus.WIN:
                    self.win()
                case _:
                    exit(0)
            self.clock.tick(100)

    def menu(self):
        size_button = (300, 100)
        position_x = (self.screen.get_width() - size_button[0]) / 2
        position_y = (self.screen.get_height() - size_button[0]) / 2

        button_normal_mode = Button("Обычный режим", GameMode.NORMAL,
                                    size_button, (position_x, position_y + 50), 24)
        button_image_mode = Button("Режим с картинкой", GameMode.IMAGE,
                                   size_button, (position_x, position_y + 200), 24)

        self.image = self.get_image()
        if not self.image:
            button_image_mode.state = ButtonState.INACTIVE

        group_buttons = ButtonGroup(button_normal_mode, button_image_mode)

        while True:
            self.screen.fill(Colors.APRICOT)

            font_title = pygame.font.Font(FONT, 74)
            title = font_title.render("Пятнашки", True, Colors.BLACKBERRY)
            title_w = title.get_width()
            title_h = title.get_height()
            self.screen.blit(title, ((WIDTH - title_w) / 2, title_h + 5))

            group_buttons.update()
            group_buttons.draw(self.screen)

            btn: Button
            if (btn := group_buttons.get_clicked()) is not None:
                self.game_status = GameStatus.GAME
                self.game_mode = btn.click_data
                pygame.event.clear()
                pygame.time.delay(200)
                break

            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                self.game_status = GameStatus.END
                break

            self.clock.tick(100)

    def game(self, *, image_path: str | None):
        place = Place(self.screen, image_path=image_path)
        self.game_status = place.game()
        self.time0, self.steps = place.get_record()

    def win(self):
        time_now = datetime.now()

        size_button = (300, 100)
        position_x = (self.screen.get_width() - size_button[0]) / 2
        position_y = self.screen.get_height() - size_button[1] * 2
        button_replay = Button("Заново", GameStatus.MENU,
                               size_button, (position_x, position_y + 50), 24)

        group_buttons = ButtonGroup(button_replay)

        game_time = time_now - self.time0
        time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds % 60 :02}"
        steps: int = self.steps

        if prev_record := self.read_record():
            prev_time, prev_steps = prev_record

            result = prev_time > game_time, prev_steps > steps
            if is_record := all(result):
                self.write_record(game_time, steps)

        elif prev_record is None:
            self.write_record(game_time, steps)
            is_record = True

        else:
            is_record = False

        while True:
            self.screen.fill(Colors.APRICOT)

            font_title = pygame.font.Font(FONT, 74)
            font = pygame.font.Font(FONT, 36)

            title = font_title.render("Пятнашки", True, Colors.BLACKBERRY)
            title_w = title.get_width()
            title_h = title.get_height()
            self.screen.blit(title, ((WIDTH - title_w) / 2, title_h + 5))

            if is_record:
                record = font.render(f"Рекорд!!!", True, Colors.BLACKBERRY)
                record_w = record.get_width()
                self.screen.blit(record, ((WIDTH - record_w) / 2, HEIGHT / 2 - 50))

            time_font = font.render(f"Время - {time_str}", True, Colors.BLACKBERRY)
            time_font_w = time_font.get_width()
            self.screen.blit(time_font, ((WIDTH - time_font_w) / 2, HEIGHT / 2))

            steps_font = font.render(f"Ходов - {steps}", True, Colors.BLACKBERRY)
            steps_font_w = steps_font.get_width()
            self.screen.blit(steps_font, ((WIDTH - steps_font_w) / 2, HEIGHT / 2 + 50))

            group_buttons.update()
            group_buttons.draw(self.screen)

            if group_buttons.get_clicked() is not None:
                self.game_status = GameStatus.MENU
                break

            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                self.game_status = GameStatus.END
                break

            self.clock.tick(100)

    @staticmethod
    def get_image() -> str | None:
        if not (exists(PATH_IMAGES) and listdir(PATH_IMAGES)):
            return

        images = listdir(PATH_IMAGES)
        shuffle(images)

        for image in images:
            image = PATH_IMAGES + "/" + image
            try:
                pygame.image.load(image)
                return image
            except pygame.error:
                continue

    @staticmethod
    def read_record() -> tuple[timedelta, int] | None:
        try:
            with open(PATH_RECORD, "r") as file:
                time = timedelta(seconds=int(file.readline()))
                steps = int(file.readline())
                return time, steps
        except (ValueError, FileNotFoundError):
            return None

    @staticmethod
    def write_record(time: timedelta, steps: int):
        with open(PATH_RECORD, "w") as file:
            file.write(
                f"{str(time.seconds)}\n{steps}"
            )

    @staticmethod
    def end():
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    Game().main_loop()
