import pygame
import json
from dataclasses import dataclass
from constants import Constants


@dataclass
class Tileset:
    tiles: list[int]
    width: int
    height: int
    index_offset: int


class Tilemap:
    def __init__(self, layers: list[Tileset]):
        self.layers = layers

    def draw_layer(
        self,
        index: int,
        screen: pygame.Surface,
        tileset_img: pygame.Surface,
        sprite_size: tuple[int, int] = (
            Constants.TILESIZE,
            Constants.TILESIZE,
        ),
        tileset_width_in_tiles: int = 22,
    ) -> None:
        for i, item in enumerate(self.layers[index].tiles):
            item_id = item - self.layers[index].index_offset
            if item_id == -1:
                continue

            tile_x = int(i % self.layers[index].width)
            tile_y = int(i / self.layers[index].width)
            pixel_x = tile_x * Constants.TILESIZE
            pixel_y = tile_y * Constants.TILESIZE

            src_x = (item_id % tileset_width_in_tiles) * sprite_size[0]
            src_y = (item_id / tileset_width_in_tiles) * sprite_size[1]

            screen.blit(
                tileset_img,
                (pixel_x, pixel_y),
                pygame.rect.Rect(
                    src_x,
                    src_y,
                    sprite_size[0],
                    sprite_size[1],
                ),
            )


def load_map(path: str) -> Tilemap:
    content = open(path)
    data = json.load(content)
    layers = []
    for i, raw_layer in enumerate(data["layers"]):
        layers.append(
            Tileset(
                tiles=raw_layer["data"],
                width=raw_layer["width"],
                height=raw_layer["height"],
                index_offset=data["tilesets"][i]["firstgid"],
            )
        )
    return Tilemap(layers=layers)


if __name__ == "__main__":
    tilemap = load_map("assets/maps/map1.json")
    print(len(tilemap.layers))
