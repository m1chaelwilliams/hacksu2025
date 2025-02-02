from pygame import Rect


class Animation:
    def __init__(self, first: int, last: int, speed: float, step=1):
        self.first = first
        self.last = last
        self.cur = self.first
        self.speed = speed
        self.duration_left = speed
        self.step = step

    def update(self, dt: float) -> None:
        self.duration_left -= dt
        if self.duration_left <= 0.0:
            self.duration_left = self.speed
            self.cur += self.step
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
