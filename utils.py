from pygame.rect import Rect
from constants import Constants
from tilemap import Tileset
import pygame


def load_img(path: str) -> pygame.Surface:
    return pygame.transform.scale_by(
        pygame.image.load(path),
        Constants.TILESIZE / Constants.IMPORT_TILESIZE,
    )


def get_hitboxes(
    layer: Tileset,
    hitbox_size: tuple[int, int],
    topleft_offset: tuple[int, int],
) -> list[Rect]:
    rects = []
    for i, item in enumerate(layer.tiles):
        item_id = item - layer.index_offset
        print(item_id)
        if item_id < 0:
            continue
        x = int(i % layer.width) * Constants.TILESIZE
        y = int(i / layer.width) * Constants.TILESIZE
        rects.append(
            Rect(
                x + topleft_offset[0],
                y + topleft_offset[1],
                hitbox_size[0],
                hitbox_size[1],
            )
        )
        print(rects[len(rects) - 1])
    return rects

