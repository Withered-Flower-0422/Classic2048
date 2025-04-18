import pygame
from pygame.typing import ColorLike

import config
from font import font


def draw_tile(
    # font settings
    content: int | str = 2,
    font_color: ColorLike = "black",
    font_size: int | None = None,
    offset_y: int | None = None,
    # tile settings
    tile_size: int = 100,
    tile_color: ColorLike = "#999999",
    # outline settings
    outline_thickness_factor: float = 0.02,
    outline_color: ColorLike = "#000000",
) -> pygame.Surface:
    surface = pygame.Surface((tile_size, tile_size))
    surface.fill(tile_color)

    if outline_thickness_factor == 0.0:
        outline_width = 0
    else:
        outline_width = max(1, int(tile_size * outline_thickness_factor))

    if outline_width > 0:
        pygame.draw.rect(
            surface,
            outline_color,
            (0, 0, tile_size, tile_size),
            outline_width,
        )

    if content == 0:
        factor = 0.0
    else:
        factors = [0.0, 1.0, 0.8, 0.6, 0.5, 0.4, 0.35, 0.3]
        font_length = len(str(content))
        factor = (
            factors[font_length] if font_length < len(factors) else factors[-1]
        ) / 1.35

    f, success = font(
        font_size if font_size is not None else int(tile_size * factor),
        font_size if font_size is not None else int(tile_size * factor * 1.35),
    )
    offset_y = offset_y if offset_y is not None else (0 if success else 6)

    text = f.render(str(content), True, font_color)
    text_rect = text.get_rect(
        center=(
            tile_size / 2,
            tile_size / 2 + offset_y * factor,
        )
    )
    surface.blit(text, text_rect)

    return surface


def draw_tile_using_config(num: int) -> pygame.Surface:
    index = num if num in config.FONT_COLOR else -1
    return draw_tile(
        content=num,
        font_color=config.FONT_COLOR[index],
        tile_size=config.TILE_SIZE,
        tile_color=config.TILE_COLOR[index],
    )


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    screen.fill(config.BG_COLOR)

    for i in range(0, 18):
        screen.blit(
            draw_tile_using_config(2**i if i != 0 else 0),
            ((i + 1) * config.TILE_SIZE, 450),
        )

    # region
    screen.blit(draw_tile(content="+", tile_size=45), (100, 700))
    screen.blit(draw_tile(content="-", tile_size=45), (200, 700))
    screen.blit(draw_tile(content="*", tile_size=45), (300, 700))
    screen.blit(draw_tile(content="/", tile_size=45), (400, 700))
    screen.blit(
        draw_tile(
            content="Col:",
            font_color="white",
            tile_size=150,
            offset_y=-50,
            tile_color=config.BG_COLOR,
            outline_thickness_factor=0,
        ),
        (500, 650),
    )
    screen.blit(draw_tile(content=2), (650, 650))
    screen.blit(
        draw_tile(
            content="Row:",
            font_color="white",
            tile_size=150,
            offset_y=-50,
            tile_color=config.BG_COLOR,
            outline_thickness_factor=0,
        ),
        (500, 800),
    )
    screen.blit(draw_tile(content=5), (650, 800))
    # endregion

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
