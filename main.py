import pygame
from pygame import Surface

from Place import Place
from variables import *


class Game:
    def __init__(self):
        pygame.init()
        self.game_status = GameStatus.MENU
        self.screen: Surface = pygame.display.set_mode((WIDTH, HEIGHT))
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
                case _:
                    print("default")
                    exit(0)

    def menu(self):
        while True:
            self.screen.fill(Colors.FOREST_WOLF)

            font = pygame.font.Font(pygame.font.get_default_font(), 36)

            title = font.render("Пятнашки", True, Colors.DARK_PURPLE)
            title_w = title.get_width()
            title_h = title.get_height()
            self.screen.blit(title, ((WIDTH - title_w) / 2, title_h + 5))

            start_text = font.render(f"Пробел - Начать!", True, Colors.DARK_PURPLE)
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
        while True:
            place.draw()

            # place.generate_place()
            # m = place.matrix
            # print(m)

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
