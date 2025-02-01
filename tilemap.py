import pygame
import json
from dataclasses import dataclass


TILESIZE = 16
NUM_TILES_PER_ROW = 22


@dataclass
class Tileset:
    tiles: list[int]
    width: int
    height: int


class Tilemap:
    def __init__(self, layers: list[Tileset]):
        self.layers = layers

    def draw(
        self,
        screen: pygame.Surface,
        tileset_img: pygame.Surface,
    ) -> None:
        for layer in self.layers:
            for i, item in enumerate(layer.tiles):
                tile_x = int(i % layer.width)
                tile_y = int(i / layer.width)
                pixel_x = tile_x * TILESIZE
                pixel_y = tile_y * TILESIZE

                src_x = ((item - 1) % NUM_TILES_PER_ROW) * TILESIZE
                src_y = ((item - 1) / NUM_TILES_PER_ROW) * TILESIZE

                screen.blit(
                    tileset_img,
                    (pixel_x, pixel_y),
                    pygame.rect.Rect(
                        src_x,
                        src_y,
                        TILESIZE,
                        TILESIZE,
                    ),
                )


def load_map(path: str) -> Tilemap:
    content = open(path)
    data = json.load(content)
    layers = []
    for raw_layer in data["layers"]:
        layers.append(
            Tileset(
                tiles=raw_layer["data"],
                width=raw_layer["width"],
                height=raw_layer["height"],
            )
        )
    return Tilemap(layers=layers)


if __name__ == "__main__":
    tilemap = load_map("assets/maps/map1.json")
    print(len(tilemap.layers))
