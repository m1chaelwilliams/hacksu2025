import pygame
from pygame.rect import Rect
from pygame.math import Vector2
from constants import Constants


class Player(pygame.sprite.Sprite):

    speed = 200

    def __init__(self, groups, init_pos: tuple[int, int]):
        self.sprite_sheet = pygame.image.load(
            "assets/characters/NinjaDark/SpriteSheet.png"
        )
        self.srect = Rect(
            0,
            0,
            16,
            16,
        )
        self.drect: Rect = Rect(
            init_pos[0] * Constants.TILESIZE,
            init_pos[1] * Constants.TILESIZE,
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
        self.hitbox_topleft_offset = (4, 4)
        self.vel = Vector2(0, 0)
        self.hitbox: Rect = Rect(
            init_pos[0] * Constants.TILESIZE + self.hitbox_topleft_offset[0],
            init_pos[1] * Constants.TILESIZE + self.hitbox_topleft_offset[1],
            Constants.TILESIZE - self.hitbox_topleft_offset[0] * 2,
            Constants.TILESIZE - self.hitbox_topleft_offset[1] * 2,
        )

    def update(self) -> None:
        self.vel.x = 0
        self.vel.y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel.y = -Player.speed
        if keys[pygame.K_a]:
            self.vel.x = -Player.speed
        if keys[pygame.K_s]:
            self.vel.y = Player.speed
        if keys[pygame.K_d]:
            self.vel.x = Player.speed

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.sprite_sheet,
            self.drect,
            self.srect,
        )

    def collides(self, rect: Rect) -> bool:
        return self.hitbox.colliderect(rect)

    def move_x(self, dt: float) -> None:
        self.drect.x += self.vel.x * dt
        self.hitbox.x += self.vel.x * dt

    def move_y(self, dt: float) -> None:
        self.drect.y += self.vel.y * dt
        self.hitbox.y += self.vel.y * dt

    def update_drect_from_hitbox(self) -> None:
        self.drect = Rect(
            self.hitbox.x - self.hitbox_topleft_offset[0],
            self.hitbox.y - self.hitbox_topleft_offset[1],
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
