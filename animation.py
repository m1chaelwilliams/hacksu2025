from pygame import Rect
from constants import Constants


class Animation:
    def __init__(self, first: int, last: int, speed: float):
        self.first = first
        self.last = last
        self.cur = self.first
        self.speed = speed
        self.duration_left = speed

    def update(self, dt: float) -> None:
        self.duration_left -= dt
        if self.duration_left <= 0.0:
            self.duration_left = self.speed
            self.cur += 1
            if self.cur > self.last:
                self.cur = self.first

    def frame(self, num_tiles_per_row: int, tilesize: int) -> Rect:
        """
        `num_tiles_per_row` is the number of tiles on a row on the tileset image
        """
        return Rect(
            int(self.cur % num_tiles_per_row) * tilesize,
            int(self.cur / num_tiles_per_row) * tilesize,
            tilesize,
            tilesize,
        )
