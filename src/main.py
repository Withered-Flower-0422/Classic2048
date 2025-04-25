import sys
import pygame
from typing import Literal

import config
from button import Button
from display import Display
from classic2048 import Classic2048
from base_path import is_dev_env, base_path
from tile_drawer import draw_tile_using_config

VERSION = "1.0.2"
AUTHOR = "Withered_Flower"


class App:
    def __init__(self):
        # initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.WINDOW_SIZE["width"], config.WINDOW_SIZE["height"])
        )
        pygame.display.set_caption("Classic 2048")
        pygame.display.set_icon(
            pygame.image.load(base_path / "assets" / "icon" / "2048.ico")
        )

        # disable text input
        pygame.key.set_text_input_rect(None)
        pygame.key.stop_text_input()

        # load sounds
        sounds_path = base_path / "assets" / "sounds"
        self.bgm = pygame.mixer.Sound(sounds_path / "bgm.ogg")
        self.slide_sound = pygame.mixer.Sound(sounds_path / "slide.wav")
        self.game_over_sound = pygame.mixer.Sound(sounds_path / "game_over.wav")
        self.bgm.set_volume(0.5)
        self.slide_sound.set_volume(0.5)
        self.game_over_sound.set_volume(0.5)
        self.hover_sound = pygame.mixer.Sound(sounds_path / "hover.ogg")
        self.click_sound = pygame.mixer.Sound(sounds_path / "click.ogg")

        self.bgm.play(-1)

        # game variables
        self.row: int = 4
        self.col: int = 4
        self.is_gaming: bool = False
        self.is_bgm_on: bool = True

        # create displays
        self.mainmenu_disps: dict[str, Display] = {
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
        self.ingame_disps: dict[str, Display] = {
            "score": Display(
                content="Score: 0",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 85,
                ),
                font_size=(20, 32),
                font_color="green",
                offset_y=(2, 6),
                disp_size=(config.WINDOW_SIZE["width"], 25),
                disp_color=config.BG_COLOR,
                outline_thickness=0,
            ),
            "game_over": Display(
                content="Game Over!",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 2.325,
                ),
                font_size=(64, 90),
                font_color="red",
                offset_y=(-6, 6),
                disp_size=(400, 100),
                disp_color="black",
                outline_thickness=0,
                alpha=196,
            ),
            "reset_tip": Display(
                content="Press R to reset",
                pos=(
                    config.WINDOW_SIZE["width"] / 2,
                    config.WINDOW_SIZE["height"] / 1.675,
                ),
                font_size=(30, 40),
                font_color="red",
                offset_y=(0, 2),
                disp_size=(300, 50),
                disp_color="black",
                outline_thickness=0,
                alpha=196,
            ),
        }

        # create buttons
        self.mainmenu_btns: dict[str, Button] = {
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
            "bgm_toggle": Button(
                content="M",
                pos=(
                    config.WINDOW_SIZE["width"] / 1.015,
                    config.WINDOW_SIZE["height"] / 1.02,
                ),
                font_size=(15, 25),
                font_color="white",
                offset_y=(-2, 0),
                disp_size=(25, 25),
                disp_color=config.BG_COLOR,
                on_enter_sound=self.hover_sound,
                on_click=self.toggle_bgm,
                on_click_sound=self.click_sound,
            ),
        }
        self.ingame_btns: dict[str, Button] = {
            "bgm_toggle": self.mainmenu_btns["bgm_toggle"],
        }

        self.game: Classic2048 | None = None

    def toggle_bgm(self) -> None:
        self.is_bgm_on = not self.is_bgm_on
        self.bgm.set_volume(0.5 if self.is_bgm_on else 0)
        self.mainmenu_btns["bgm_toggle"].font_color = (
            "white" if self.is_bgm_on else "black"
        )

    def start_game(self) -> None:
        self.game = Classic2048(self.row, self.col)
        self.is_gaming = True

    def change_row_col(
        self,
        which: Literal["row", "col"],
        increment: Literal[1, -1],
    ) -> None:
        # helper functions
        def clip(num: int, min_val: int, max_val: int) -> int:
            return max(min(num, max_val), min_val)

        match which:
            case "row":
                self.row += increment
                self.row = clip(self.row, 2, 6)
                self.mainmenu_disps["row_disp"].content = str(self.row)
            case "col":
                self.col += increment
                self.col = clip(self.col, 2, 9)
                self.mainmenu_disps["col_disp"].content = str(self.col)

    def handle_events(self) -> None:
        # helper functions
        def handle_mainmenu_events() -> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_m:
                        self.toggle_bgm()
                        self.click_sound.play()
                    else:
                        for params, keys in {
                            ("col", -1): (pygame.K_LEFT, pygame.K_a),
                            ("col", 1): (pygame.K_RIGHT, pygame.K_d),
                            ("row", 1): (pygame.K_UP, pygame.K_w),
                            ("row", -1): (pygame.K_DOWN, pygame.K_s),
                        }.items():
                            if event.key in keys:
                                self.change_row_col(*params)
                                self.click_sound.play()
                                break
                for btn in self.mainmenu_btns.values():
                    btn.handle_events(event)

            self.update_display()

        def handle_game_events() -> None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.is_gaming = False
                    elif event.key == pygame.K_m:
                        self.toggle_bgm()
                        self.click_sound.play()
                    elif is_dev_env and event.key == pygame.K_F2:
                        self.game.game_over = True
                    else:
                        for direction, keys in {
                            "left": (pygame.K_LEFT, pygame.K_a),
                            "right": (pygame.K_RIGHT, pygame.K_d),
                            "up": (pygame.K_UP, pygame.K_w),
                            "down": (pygame.K_DOWN, pygame.K_s),
                        }.items():
                            if event.key in keys:
                                if self.game.move(direction):
                                    if self.game.game_over:
                                        self.game_over_sound.play()
                                    else:
                                        self.slide_sound.play()
                                break

                for btn in self.ingame_btns.values():
                    btn.handle_events(event)

                self.update_display()

        handle_game_events() if self.is_gaming else handle_mainmenu_events()

    def update_display(self) -> None:
        # helper functions
        def update_mainmenu_display() -> None:
            for disp in self.mainmenu_disps.values():
                disp.draw(self.screen)
            for btn in self.mainmenu_btns.values():
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

            # draw score
            self.ingame_disps["score"].content = f"Score: {self.game.cal_score()}"
            self.ingame_disps["score"].draw(self.screen)

            # draw game over
            if self.game.game_over:
                self.ingame_disps["game_over"].draw(self.screen)
                self.ingame_disps["reset_tip"].draw(self.screen)

            # draw buttons
            for btn in self.ingame_btns.values():
                btn.draw(self.screen)

        self.screen.fill(config.BG_COLOR)
        update_game_display() if self.is_gaming else update_mainmenu_display()
        pygame.display.update()

    def run(self):
        self.update_display()
        while True:
            self.handle_events()


if __name__ == "__main__":
    App().run()
