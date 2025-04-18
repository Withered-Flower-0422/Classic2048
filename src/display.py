import pygame
from pygame.typing import ColorLike

from font import font


class Display:
    def __init__(
        self,
        # basic settings
        content: str = "Display",
        pos: tuple[int, int] = (150, 50),
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
    ):
        self.content = content
        self.pos = (pos[0] - disp_size[0] / 2, pos[1] - disp_size[1] / 2)
        self.font_size = font_size
        self.font_color = font_color
        self.offset_y = offset_y
        self.disp_size = disp_size
        self.disp_color = disp_color
        self.outline_thickness = outline_thickness
        self.outline_color = outline_color

        self.update_surface()

    def update_surface(self) -> None:
        surface = pygame.Surface(self.disp_size)
        surface.fill(self.disp_color)
        if self.outline_thickness > 0:
            pygame.draw.rect(
                surface,
                self.outline_color,
                (0, 0, *self.disp_size),
                self.outline_thickness,
            )

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

        self.surface = surface

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.pos)


if __name__ == "__main__":
    import config

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen.fill(config.BG_COLOR)

    Display().draw(screen)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
