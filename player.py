import pygame
from constants import Constants


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, init_pos: tuple[int, int]):
        self.drect = pygame.rect.Rect(
            init_pos[0] * Constants.TILESIZE,
            init_pos[1] * Constants.TILESIZE,
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
        self.hitbox = self.drect.copy()
