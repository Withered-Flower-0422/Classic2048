import pygame
from typing import Callable
from pygame.typing import ColorLike

from display import Display


class Button(Display):
    def __init__(
        self,
        # basic settings
        content: str = "Button",
        pos: tuple[int, int] = (150, 50),
        # font settings
        font_size: tuple[int, int] = (60, 100),  # [normal, backup]
        font_color: ColorLike = "black",
        offset_y: tuple[int, int] = (-6, 6),  # [normal, backup]
        # display settings
        disp_size: tuple[int, int] = (300, 100),
        disp_color: ColorLike = "#999999",
        disp_color_on_hover: ColorLike = "lightgreen",
        disp_color_on_click: ColorLike = "green",
        # on_click settings
        on_click: Callable = lambda: print("Button clicked!"),
        # outline settings
        outline_thickness: int = 2,
        outline_color: ColorLike = "black",
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
        )
        self.disp_color_original = disp_color
        self.disp_color_on_hover = disp_color_on_hover
        self.disp_color_on_click = disp_color_on_click
        self.on_click = on_click
        self.is_clicked: bool = False

        self.update_surface()

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Return the value returned by the on_click function if the button is clicked, None otherwise.
        """

        val = None

        abs_rect = self.surface.get_rect().move(self.pos)

        # hover event
        if event.type == pygame.MOUSEMOTION and not self.is_clicked:
            if abs_rect.collidepoint(event.pos):
                self.disp_color = self.disp_color_on_hover
            else:
                self.disp_color = self.disp_color_original

        # click event
        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and abs_rect.collidepoint(event.pos)
        ):
            self.is_clicked = True
            self.disp_color = self.disp_color_on_click

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_clicked:
                if abs_rect.collidepoint(event.pos):
                    val = self.on_click()
                self.is_clicked = False
                if abs_rect.collidepoint(event.pos):
                    self.disp_color = self.disp_color_on_hover
                else:
                    self.disp_color = self.disp_color_original

        self.update_surface()

        return val


if __name__ == "__main__":
    import config

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen.fill(config.BG_COLOR)

    def f1():
        print("f1 called")
        return 1

    def f2():
        print("f2 called")
        return 2

    btn1 = Button(on_click=f1)
    btn2 = Button(
        content="Button 2",
        pos=(250, 100),
        on_click=f2,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            v1 = btn1.handle_event(event)
            btn1.draw(screen)
            v2 = btn2.handle_event(event)
            btn2.draw(screen)
            if v1 is not None:
                print(v1)
            if v2 is not None:
                print(v2)
        pygame.display.update()
