import pygame
import warnings

warnings.filterwarnings("error", category=UserWarning)


def font(size: int, size_backup: int) -> tuple[pygame.font.Font, bool]:
    """
    Try to load system font "comicsansms" with given size.
    If failed, load default pygame font with given size_backup.
    True will be returned if system font loaded successfully, False otherwise.
    """
    try:
        return pygame.font.SysFont("comicsansms", size), True
    except UserWarning:
        return pygame.font.Font(None, size_backup), False


if __name__ == "__main__":
    pygame.init()
    print(font(30, 20))
