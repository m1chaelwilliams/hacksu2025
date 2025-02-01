import pygame
import json
from dataclasses import dataclass


# @dataclass
# class TilesetDesc:
#     num_tiles_per_row: int
#     tilesize: int
#
#
# class Tile:
#     def __init__(self, id: int, tileset_desc: TilesetDesc):
#         self.id = id - 1
#         self.rect = pygame.rect.Rect(
#             (self.id % tileset_desc.num_tiles_per_row) * tileset_desc.tilesize,
#             (self.id / tileset_desc.num_tiles_per_row) * tileset_desc.num_tiles_per_row,
#             tileset_desc.tilesize,
#             tileset_desc.tilesize,
#         )
#


class Tilemap:
    def __init__(self, layers: list[list[int]]):
        self.layers = layers


def load_map(path: str) -> list[int]:
    content = open(path)
    data = json.load(content)
    layers = []
    print(data["layers"])
    pass


if __name__ == "__main__":
    load_map("assets/maps/map1.json")
