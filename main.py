from datetime import datetime

import pygame
from pygame import Surface

from Place import Place
from variables import *


class Game:
    def __init__(self):
        pygame.init()
        self.game_status = GameStatus.MENU
        self.screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))

        self.time0 = None
        self.steps = None

        pygame.display.set_caption(NAME)

    def main_loop(self):
        while True:
            match self.game_status:
                case GameStatus.MENU:
                    self.menu()
                case GameStatus.GAME:
                    self.game()
                case GameStatus.END:
                    self.end()
                case GameStatus.WIN:
                    self.win()
                case _:
                    exit(0)

    def menu(self):
        while True:
            self.screen.fill(Colors.APRICOT)

            font = pygame.font.Font(FONT, 52)

            title = font.render("Пятнашки", True, Colors.BLACKBERRY)
            title_w = title.get_width()
            title_h = title.get_height()
            self.screen.blit(title, ((WIDTH - title_w) / 2, title_h + 5))

            start_text = font.render(f"Пробел - Начать!", True, Colors.BLACKBERRY)
            start_text_w = start_text.get_width() / 2
            self.screen.blit(start_text, (WIDTH / 2 - start_text_w, HEIGHT / 2))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_status = GameStatus.GAME
                break

            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                self.game_status = GameStatus.END
                break

    def game(self):
        place = Place(self.screen)
        place.generate_place()
        while True:
            place.draw()
            if place.check_win():
                self.game_status = GameStatus.WIN
                self.time0, self.steps = place.get_record()
                break

            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                self.game_status = GameStatus.END
                break
            elif pygame.event.get(pygame.MOUSEBUTTONUP):
                place.click()

    def win(self):
        time_now = datetime.now()
        while True:
            self.screen.fill(Colors.APRICOT)

            font = pygame.font.Font(FONT, 36)

            title = font.render("Пятнашки", True, Colors.BLACKBERRY)
            title_w = title.get_width()
            title_h = title.get_height()
            self.screen.blit(title, ((WIDTH - title_w) / 2, title_h + 5))

            game_time = time_now - self.time0
            time_str = f"{game_time.seconds // 60 :02}:{game_time.seconds % 60 :02}"
            steps = self.steps

            record = font.render(f"Рекорд", True, Colors.BLACKBERRY)
            record_w = record.get_width()
            self.screen.blit(record, ((WIDTH - record_w) / 2, HEIGHT / 2 - 50))

            time_font = font.render(f"Время: {time_str}", True, Colors.BLACKBERRY)
            time_font_w = time_font.get_width()
            self.screen.blit(time_font, ((WIDTH - time_font_w) / 2, HEIGHT / 2))

            steps_font = font.render(f"Ходов: {steps}", True, Colors.BLACKBERRY)
            steps_font_w = steps_font.get_width()
            self.screen.blit(steps_font, ((WIDTH - steps_font_w) / 2, HEIGHT / 2 + 50))

            start_text = font.render(f"Пробел - Заново!", True, Colors.BLACKBERRY)
            start_text_w = start_text.get_width() / 2
            start_text_h = start_text.get_height()
            self.screen.blit(start_text, (WIDTH / 2 - start_text_w, HEIGHT - start_text_h))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.game_status = GameStatus.GAME
                break

            pygame.display.update()
            if pygame.event.get(pygame.QUIT):
                self.game_status = GameStatus.END
                break

    @staticmethod
    def end():
        pygame.quit()
        exit(0)


if __name__ == '__main__':
    Game().main_loop()
