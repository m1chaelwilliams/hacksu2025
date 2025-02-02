import pygame
from pygame import Rect
from pygame.math import Vector2
from constants import Constants
from animation import Animation


class Projectile:

    lifespan = 5

    def __init__(
        self,
        pos: tuple[int, int],
        dir: Vector2,
        speed: float,
        img: pygame.Surface,
        anim: Animation,
    ):
        self.drect = Rect(
            pos[0],
            pos[1],
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
        self.dir = dir
        self.speed = speed
        self.lifespan = Projectile.lifespan
        self.alive = True
        self.img = img
        self.img_num_tiles_per_row = int(self.img.width / Constants.TILESIZE)
        self.anim = anim

    def update(self, dt: float) -> None:
        self.anim.update(dt)
        self.lifespan -= dt
        if self.lifespan < 0.0:
            self.lifespan = 0.0
            self.alive = False

    def move_x(self, dt: float) -> None:
        self.drect.x += self.dir.x * self.speed * dt

    def move_y(self, dt: float) -> None:
        self.drect.y += self.dir.y * self.speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        # DEBUG RECT BELOW
        # pygame.draw.rect(
        #     screen,
        #     (255, 0, 0),
        #     self.drect,
        #     1,
        # )
        screen.blit(
            self.img,
            self.drect,
            self.anim.frame(self.img_num_tiles_per_row, Constants.TILESIZE),
        )
