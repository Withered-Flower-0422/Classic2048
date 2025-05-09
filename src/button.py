import pygame
from typing import Callable, Any
from pygame.typing import ColorLike

from display import Display

type Params = tuple[tuple[Any, ...], dict[str, Any]]


class Button(Display):
    def __init__(
        self,
        # basic settings
        content: str | pygame.Surface = "Button",
        pos: tuple[float, float] = (150, 50),
        # font settings
        font_size: tuple[int, int] = (60, 100),  # [normal, backup]
        font_color: ColorLike = "black",
        offset_y: tuple[int, int] = (-6, 6),  # [normal, backup]
        # display settings
        disp_size: tuple[int, int] = (300, 100),
        disp_color: ColorLike = "#999999",
        disp_color_on_hover: ColorLike = "lightgreen",
        disp_color_on_click: ColorLike = "green",
        # outline settings
        outline_thickness: int = 2,
        outline_color: ColorLike = "black",
        # alpha settings
        alpha: int = 255,
        # events settings
        on_enter: Callable = lambda: None,
        on_enter_params: Params | None = None,
        on_enter_sound: pygame.mixer.Sound | None = None,
        on_click: Callable = lambda: print("Button clicked!"),
        on_click_params: Params | None = None,
        on_click_sound: pygame.mixer.Sound | None = None,
        on_exit: Callable = lambda: None,
        on_exit_params: Params | None = None,
        on_exit_sound: pygame.mixer.Sound | None = None,
    ):
        super().__init__(
            content,
            pos,
            font_size,
            font_color,
            offset_y,
            disp_size,
            disp_color,
            outline_thickness,
            outline_color,
            alpha,
        )
        self.disp_color_original = disp_color
        self.disp_color_on_hover = disp_color_on_hover
        self.disp_color_on_click = disp_color_on_click
        self.on_enter = on_enter
        self.on_enter_params: Params = (
            on_enter_params if on_enter_params is not None else ((), {})
        )
        self.on_enter_sound = on_enter_sound
        self.on_click = on_click
        self.on_click_params: Params = (
            on_click_params if on_click_params is not None else ((), {})
        )
        self.on_click_sound = on_click_sound
        self.on_exit = on_exit
        self.on_exit_params: Params = (
            on_exit_params if on_exit_params is not None else ((), {})
        )
        self.on_exit_sound = on_exit_sound

        self.is_hovered: bool = False
        self.is_clicked: bool = False

    def handle_events(self, event: pygame.event.Event) -> tuple[Any, Any, Any]:
        """
        Returns a tuple containing the return values (default is None) of
        `on_enter`, `on_click`, and `on_exit` functions if they are called.
        The order of the return values is (`on_enter`, `on_click`, `on_exit`).
        """

        # helper functions
        def handle_on_enter() -> Any:
            ret = None

            if not self.is_hovered and abs_rect.collidepoint(pygame.mouse.get_pos()):
                self.is_hovered = True
                self.disp_color = self.disp_color_on_hover
                if self.on_enter_sound:
                    self.on_enter_sound.play()
                ret = self.on_enter(*self.on_enter_params[0], **self.on_enter_params[1])

            return ret

        def handle_on_click() -> Any:
            ret = None

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and abs_rect.collidepoint(event.pos)
            ):
                self.is_clicked = True
                self.disp_color = self.disp_color_on_click

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.is_clicked:
                    if abs_rect.collidepoint(event.pos):
                        if self.on_click_sound:
                            self.on_click_sound.play()
                        ret = self.on_click(
                            *self.on_click_params[0], **self.on_click_params[1]
                        )
                    self.is_clicked = False
                    if abs_rect.collidepoint(event.pos):
                        self.disp_color = self.disp_color_on_hover
                    else:
                        self.disp_color = self.disp_color_original

            return ret

        def handle_on_exit() -> Any:
            ret = None

            if self.is_hovered and not abs_rect.collidepoint(pygame.mouse.get_pos()):
                self.is_hovered = False
                self.disp_color = self.disp_color_original
                if self.on_exit_sound:
                    self.on_exit_sound.play()
                ret = self.on_exit(*self.on_exit_params[0], **self.on_exit_params[1])

            return ret

        abs_rect = self.surface.get_rect().move(
            (
                self.pos[0] - self.disp_size[0] / 2,
                self.pos[1] - self.disp_size[1] / 2,
            )
        )

        return handle_on_enter(), handle_on_click(), handle_on_exit()


if __name__ == "__main__":
    from random import randint

    import config
    from base_path import base_path

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen.fill(config.BG_COLOR)

    enter_sound = pygame.mixer.Sound(base_path / "assets" / "sounds" / "hover.ogg")
    click_sound = pygame.mixer.Sound(base_path / "assets" / "sounds" / "click.ogg")
    exit_sound = pygame.mixer.Sound(base_path / "assets" / "sounds" / "hover.ogg")

    def b1_on_enter(param):
        print("b1 entered")
        return param

    def b1_on_click(param):
        print("b1 clicked")
        return param

    def b1_on_exit(param):
        print("b1 exited")
        return param

    def b2_on_enter(param):
        print("b2 entered")
        return param

    def b2_on_click(param):
        print("b2 clicked")
        btn2.pos = (randint(100, 1800), randint(100, 900))
        return param

    def b2_on_exit(param):
        print("b2 exited")
        return param

    btn1 = Button(
        on_enter=b1_on_enter,
        on_enter_params=(("b1_enter_param",), {}),
        on_enter_sound=enter_sound,
        on_click=b1_on_click,
        on_click_params=(("b1_click_param",), {}),
        on_click_sound=click_sound,
        on_exit=b1_on_exit,
        on_exit_params=(("b1_exit_param",), {}),
        on_exit_sound=exit_sound,
    )
    btn2 = Button(
        content="Jump!!!",
        pos=(250, 100),
        # events settings
        on_enter=b2_on_enter,
        on_enter_params=(("b2_enter_param",), {}),
        on_enter_sound=enter_sound,
        on_click=b2_on_click,
        on_click_params=(("b2_click_param",), {}),
        on_click_sound=click_sound,
        on_exit=b2_on_exit,
        on_exit_params=(("b2_exit_param",), {}),
        on_exit_sound=exit_sound,
    )

    while True:
        screen.fill(config.BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            v11, v12, v13 = btn1.handle_events(event)
            v21, v22, v23 = btn2.handle_events(event)
            for v in [v11, v12, v13, v21, v22, v23]:
                if v is not None:
                    print(v)

        btn1.draw(screen)
        btn2.draw(screen)

        pygame.display.update()
