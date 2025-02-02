import pygame
from pygame.rect import Rect
from pygame.math import Vector2
from constants import Constants
import random


def random_spawn_location() -> tuple[int, int]:
    location = random.randint(1, 4)
    if location == 1:
        # top
        return (5, 0)
    elif location == 2:
        # right
        return (5, 5)
    elif location == 3:
        # bottom
        return (5, 5)
    elif location == 4:
        # left
        return (5, 5)


class Enemy(pygame.sprite.Sprite):
    zombie_speed = 100
    def __init__(self, x: int, 
                y: int, 
                width: int, 
                height: int, 
                direction: Vector2 = Vector2(0, 1), 
                health: int = 10,
                init_pos: tuple[int, int] = (5, 5)
                ):
        super().__init__()

        self.srect = Rect(0, 0, 16, 16)
        self.direction = direction
        self.vel = Vector2(0, 0)
        self.max_health = health
        self.curr_health = health
        init_pos = random_spawn_location()
        self.drect = Rect(
            # 
            init_pos[0] * Constants.TILESIZE,
            init_pos[1] * Constants.TILESIZE,
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
        self.hitbox_topleft_offset = (4, 4)
        self.hitbox = Rect(
            self.drect.x + self.hitbox_topleft_offset[0],
            self.drect.y + self.hitbox_topleft_offset[1],
            Constants.TILESIZE - self.hitbox_topleft_offset[0] * 2,
            Constants.TILESIZE - self.hitbox_topleft_offset[1] * 2,
        )

        # Placeholder sprite if none provided
        self.sprite_sheet = pygame.Surface((16, 16))
        self.sprite_sheet.fill((255, 0, 0))  # Red box for debugging

    def update(self, events: list[pygame.event.Event]) -> None:
        count = 0




    def move_x(self, dt: float) -> None:
        self.drect.x += self.vel.x * dt
        self.hitbox.x += self.vel.x * dt

    def move_y(self, dt: float) -> None:
        self.drect.y += self.vel.y * dt
        self.hitbox.y += self.vel.y * dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.sprite_sheet, self.drect, self.srect)

    def on_damage(self, damageAmt: int) -> None:
        self.curr_health -= damageAmt
        if self.curr_health <= 0:
            self.destroy()

    def get_hitbox(self) -> Rect:
        return self.hitbox

class Zombie(Enemy):
    def __init__(self, x, y, width, height, speed=1, health=15):
        super().__init__(x, y, width, height, Vector2(0, 1), speed, health)
        self.attack_power = 5
        self.sprite_sheet = pygame.image.load(
            "assets/characters/NinjaDark/SpriteSheet.png"
        )

    def load_sprite(self, sprite_path: str) -> None:
        self.sprite_sheet = pygame.image.load(sprite_path)

    def follow_player(self, player: Rect, dt: float) -> None:
        if player.x > self.drect.x:
            self.vel.x = self.zombie_speed 
        elif player.x < self.drect.x:
            self.vel.x = -self.zombie_speed
        else:
            self.vel.x = 0

        if player.y > self.drect.y:
            self.vel.y = self.zombie_speed
        elif player.y < self.drect.y:
            self.vel.y = -self.zombie_speed 
        else:
            self.vel.y = 0 

    