import pygame
from pygame.typing import ColorLike

from font import font


class Display:
    def __init__(
        self,
        # basic settings
        content: str | pygame.Surface = "Display",
        pos: tuple[float, float] = (150, 50),
        # font settings
        font_size: tuple[int, int] = (60, 100),  # [normal, backup]
        font_color: ColorLike = "black",
        offset_y: tuple[int, int] = (-6, 6),  # [normal, backup]
        # display settings
        disp_size: tuple[int, int] = (300, 100),
        disp_color: ColorLike = "#999999",
        # outline settings
        outline_thickness: int = 2,
        outline_color: ColorLike = "black",
        # alpha settings
        alpha: int = 255,
    ):
        self.content = content
        self.pos = pos
        self.font_size = font_size
        self.font_color = font_color
        self.offset_y = offset_y
        self.disp_size = disp_size
        self.disp_color = disp_color
        self.outline_thickness = outline_thickness
        self.outline_color = outline_color
        self.alpha = alpha

        self.update_surface()

    def update_surface(self) -> None:
        surface = pygame.Surface(self.disp_size)
        surface.fill(self.disp_color)

        if isinstance(self.content, str):
            f, success = font(*self.font_size)
            o = self.offset_y[0] if success else self.offset_y[1]
            text = f.render(self.content, True, self.font_color)
            text_rect = text.get_rect(
                center=(
                    self.disp_size[0] / 2,
                    self.disp_size[1] / 2 + o,
                )
            )
            surface.blit(text, text_rect)
        else:  # type(self.content) is pygame.Surface
            surface.blit(
                self.content,
                (
                    (self.disp_size[0] - self.content.get_width()) / 2,
                    (self.disp_size[1] - self.content.get_height()) / 2,
                ),
            )

        if self.outline_thickness > 0:
            pygame.draw.rect(
                surface,
                self.outline_color,
                (0, 0, *self.disp_size),
                self.outline_thickness,
            )

        surface.set_alpha(self.alpha)
        self.surface = surface

    def draw(self, screen: pygame.Surface, update_before_draw: bool = True) -> None:
        if update_before_draw:
            self.update_surface()
        screen.blit(
            self.surface,
            (
                self.pos[0] - self.disp_size[0] / 2,
                self.pos[1] - self.disp_size[1] / 2,
            ),
        )


if __name__ == "__main__":
    import config
    from base_path import base_path

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen.fill(config.BG_COLOR)

    Display(
        content=pygame.image.load(base_path / "assets" / "icon" / "2048.ico"), alpha=128
    ).draw(screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
