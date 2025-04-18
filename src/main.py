import sys
import pygame
from typing import Literal

import config
from font import font
from button import Button
from display import Display
from base_path import base_path
from classic2048 import Classic2048
from tile_drawer import draw_tile_using_config

VERSION = "1.0.1"
AUTHOR = "Withered_Flower"


class App:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_SIZE["width"], config.WINDOW_SIZE["height"])
        )
        pygame.display.set_caption("Classic 2048")
        pygame.display.set_icon(pygame.image.load(base_path / "icon" / "2048.ico"))

        # disable text input
        pygame.key.set_text_input_rect(None)
        pygame.key.stop_text_input()

        # load sounds
        self.slide_sound = pygame.mixer.Sound(base_path / "sounds" / "slide.wav")
        self.game_over_sound = pygame.mixer.Sound(
            base_path / "sounds" / "game_over.wav"
        )
        self.slide_sound.set_volume(0.5)
        self.game_over_sound.set_volume(0.5)
        self.hover_sound = pygame.mixer.Sound(base_path / "sounds" / "hover.ogg")
        self.click_sound = pygame.mixer.Sound(base_path / "sounds" / "click.ogg")

        # game variables
        self.row: int = 4
        self.col: int = 4
        self.is_gaming: bool = False

        # create displays
        self.disps: dict[str, Display] = {
            "title": Display(
                content="Classic 2048",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 8,
                ),
                font_size=(120, 170),
                font_color="lightgreen",
                offset_y=(-6, 6),
                disp_size=(800, 150),
                disp_color=config.BG_COLOR,
                outline_thickness=0,
            ),
            "col_text": Display(
                content="Col: ",
                pos=(
                    config.WINDOW_SIZE["width"] / 2.45,
                    config.WINDOW_SIZE["height"] / 2.75,
                ),
                font_size=(60, 100),
                font_color="lightskyblue",
                offset_y=(-6, 6),
                disp_size=(200, 100),
                disp_color=config.BG_COLOR,
                outline_thickness=0,
            ),
            "col_disp": Display(
                content=f"{self.col}",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.75,
                    config.WINDOW_SIZE["height"] / 2.75,
                ),
                font_size=(75, 100),
                font_color="black",
                offset_y=(-6, 6),
                disp_size=(100, 100),
                disp_color=config.TILE_COLOR[2],
            ),
            "row_text": Display(
                content="Row: ",
                pos=(
                    config.WINDOW_SIZE["width"] / 2.45,
                    config.WINDOW_SIZE["height"] / 1.65,
                ),
                font_size=(60, 100),
                font_color="cyan",
                offset_y=(-6, 6),
                disp_size=(200, 100),
                disp_color=config.BG_COLOR,
                outline_thickness=0,
            ),
            "row_disp": Display(
                content=f"{self.row}",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.75,
                    config.WINDOW_SIZE["height"] / 1.65,
                ),
                font_size=(75, 100),
                font_color="white",
                offset_y=(-6, 6),
                disp_size=(100, 100),
                disp_color=config.TILE_COLOR[8],
            ),
            "version": Display(
                content=f"Ver. {VERSION}",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 1.035,
                ),
                font_size=(20, 30),
                font_color="white",
                offset_y=(-6, 6),
                disp_size=(800, 150),
                disp_color=config.BG_COLOR,
                outline_thickness=0,
            ),
        }

        # create buttons
        self.btns: dict[str, Button] = {
            "col_up": Button(
                content="+",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.5,
                    config.WINDOW_SIZE["height"] / 3.15,
                ),
                font_size=(60, 80),
                font_color="blue",
                offset_y=(-6, -1),
                disp_size=(45, 45),
                on_enter_sound=self.hover_sound,
                on_click=self.change_row_col,
                on_click_params=(("col", 1), {}),
                on_click_sound=self.click_sound,
            ),
            "col_down": Button(
                content="-",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.5,
                    config.WINDOW_SIZE["height"] / 2.425,
                ),
                font_size=(60, 80),
                font_color="orange",
                offset_y=(-6, 1),
                disp_size=(45, 45),
                on_enter_sound=self.hover_sound,
                on_click=self.change_row_col,
                on_click_params=(("col", -1), {}),
                on_click_sound=self.click_sound,
            ),
            "row_up": Button(
                content="+",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.5,
                    config.WINDOW_SIZE["height"] / 1.8,
                ),
                font_size=(60, 80),
                font_color="white",
                offset_y=(-6, -1),
                disp_size=(45, 45),
                on_enter_sound=self.hover_sound,
                on_click=self.change_row_col,
                on_click_params=(("row", 1), {}),
                on_click_sound=self.click_sound,
            ),
            "row_down": Button(
                content="-",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.5,
                    config.WINDOW_SIZE["height"] / 1.525,
                ),
                font_size=(60, 80),
                font_color="black",
                offset_y=(-6, 1),
                disp_size=(45, 45),
                on_enter_sound=self.hover_sound,
                on_click=self.change_row_col,
                on_click_params=(("row", -1), {}),
                on_click_sound=self.click_sound,
            ),
            "start": Button(
                content="Start",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 1.2,
                ),
                font_size=(60, 100),
                font_color="magenta",
                offset_y=(-6, 6),
                disp_size=(200, 100),
                disp_color=config.BG_COLOR,
                on_enter_sound=self.hover_sound,
                on_click=self.start_game,
                on_click_sound=self.click_sound,
            ),
        }

        self.game: Classic2048 | None = None

    def start_game(self) -> None:
        self.game = Classic2048(self.row, self.col)
        self.is_gaming = True

    def change_row_col(
        self,
        which: Literal["row", "col"],
        increment: Literal[1, -1],
    ) -> bool:
        """
        Return True if the value of row or col is changed, False otherwise.
        """

        # helper functions
        def clip(num: int, min_val: int, max_val: int) -> int:
            return max(min(num, max_val), min_val)

        match which:
            case "row":
                old_val = self.row
                self.row += increment
                self.row = clip(self.row, 2, 6)
                self.disps["row_disp"].content = f"{self.row}"
                return self.row != old_val
            case "col":
                old_val = self.col
                self.col += increment
                self.col = clip(self.col, 2, 9)
                self.disps["col_disp"].content = f"{self.col}"
                return self.col != old_val

    def handle_events(self) -> None:
        # helper functions
        def handle_mainmenu_events() -> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for btn in self.btns.values():
                    btn.handle_events(event)

            self.update_display()

        def handle_game_events() -> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    for direction, key in {
                        "left": pygame.K_LEFT,
                        "right": pygame.K_RIGHT,
                        "up": pygame.K_UP,
                        "down": pygame.K_DOWN,
                    }.items():
                        if event.key == key:
                            if self.game.move(direction):
                                if self.game.game_over:
                                    self.game_over_sound.play()
                                else:
                                    self.slide_sound.play()
                            break
                    if event.key == pygame.K_r:
                        self.is_gaming = False
                    self.update_display()

        handle_game_events() if self.is_gaming else handle_mainmenu_events()

    def update_display(self) -> None:
        # helper functions
        def update_mainmenu_display() -> None:
            for disp in self.disps.values():
                disp.draw(self.screen)
            for btn in self.btns.values():
                btn.draw(self.screen)

        def update_game_display() -> None:
            # draw board
            for i in range(self.game.row):
                for j in range(self.game.col):
                    self.screen.blit(
                        draw_tile_using_config(self.game.board[i][j]),
                        (
                            config.WINDOW_SIZE["width"] / 2
                            + (j - self.game.col / 2) * config.TILE_SIZE,
                            config.WINDOW_SIZE["height"] / 2
                            + (i - self.game.row / 2) * config.TILE_SIZE,
                        ),
                    )

            # region -> draw score
            score_text = f"Score: {self.game.cal_score()}"
            score_font, _ = font(18, 32)
            score_surface = score_font.render(score_text, True, "green")
            score_rect = score_surface.get_rect(topleft=(0, 0))
            self.screen.blit(score_surface, score_rect)
            # endregion

            # draw game over
            if self.game.is_game_over():
                game_over_text = "Game Over!"
                game_over_font, _ = font(64, 72)
                game_over_surface = game_over_font.render(game_over_text, True, "red")
                game_over_rect = game_over_surface.get_rect(
                    center=(
                        config.WINDOW_SIZE["width"] / 2,
                        config.WINDOW_SIZE["height"] / 2,
                    )
                )
                self.screen.blit(game_over_surface, game_over_rect)

        self.screen.fill(config.BG_COLOR)
        update_game_display() if self.is_gaming else update_mainmenu_display()
        pygame.display.update()

    def run(self):
        self.update_display()
        while True:
            self.handle_events()


if __name__ == "__main__":
    App().run()
