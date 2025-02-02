import pygame
from pygame import Rect
from pygame.math import Vector2
from constants import Constants


class Projectile:

    def __init__(self, pos: tuple[int, int], dir: Vector2, speed: float):
        self.drect = Rect(
            pos[0],
            pos[1],
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
        self.dir = dir
        self.speed = speed

    def move_x(self, dt: float) -> None:
        self.drect.x += self.dir.x * self.speed * dt

    def move_y(self, dt: float) -> None:
        self.drect.y += self.dir.y * self.speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            self.drect,
            1,
        )
