import pygame
from pygame.rect import Rect
from pygame.math import Vector2
from constants import Constants
import random
import utils
from animation import Animation


def random_spawn_location() -> tuple[int, int]:
    location = random.randint(1, 4)
    if location == 1:
        # top
        return (7, 0)
    elif location == 2:
        # right
        return (20, 5)
    elif location == 3:
        # bottom
        return (0, 15)
    elif location == 4:
        # left
        return (20, 20)


class EnemyMovementState:
    Idle = 10
    Running = 20


class EnemyDirection:
    Left = 0
    Right = 1
    Up = 2
    Down = 3


class Enemy(pygame.sprite.Sprite):
    zombie_speed = 100

    def __init__(
        self,
        x: int,
        y: int,
        direction: Vector2 = Vector2(0, 1),
        health: int = 10,
        init_pos: tuple[int, int] = (5, 5),
    ):
        super().__init__()

        self.srect = Rect(0, 0, Constants.TILESIZE, Constants.TILESIZE)
        self.direction = direction
        self.vel = Vector2(0, 0)
        self.max_health = health
        self.curr_health = health
        init_pos = (x, y)
        self.drect = Rect(
            #
            init_pos[0],
            init_pos[1],
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
        self.sprite_sheet = pygame.Surface((Constants.TILESIZE, Constants.TILESIZE))
        self.sprite_sheet.fill((255, 0, 0))  # Red box for debugging
        self.alive = True

        self.animations: dict[int, Animation] = {
            EnemyDirection.Down + EnemyMovementState.Idle: Animation(0, 1, 100),
            EnemyDirection.Up + EnemyMovementState.Idle: Animation(1, 2, 100),
            EnemyDirection.Left + EnemyMovementState.Idle: Animation(2, 3, 100),
            EnemyDirection.Right + EnemyMovementState.Idle: Animation(3, 4, 100),
            EnemyDirection.Down + EnemyMovementState.Running: Animation(0, 12, 0.1, 4),
            EnemyDirection.Up + EnemyMovementState.Running: Animation(1, 13, 0.1, 4),
            EnemyDirection.Left + EnemyMovementState.Running: Animation(2, 14, 0.1, 4),
            EnemyDirection.Right + EnemyMovementState.Running: Animation(3, 15, 0.1, 4),
        }
        self.direction: EnemyDirection = EnemyDirection.Down
        self.movement_state: EnemyMovementState = EnemyMovementState.Idle

    def update(self, dt: float, events: list[pygame.event.Event]) -> None:
        self.animations[self.direction + self.movement_state].update(dt)

    def move_x(self, dt: float) -> None:
        self.drect.x += self.vel.x * dt
        self.hitbox.x += self.vel.x * dt

    def move_y(self, dt: float) -> None:
        self.drect.y += self.vel.y * dt
        self.hitbox.y += self.vel.y * dt

    def collides(self, rect: Rect) -> bool:
        return self.hitbox.colliderect(rect)

    def update_drect_from_hitbox(self) -> None:
        self.drect = Rect(
            self.hitbox.x - self.hitbox_topleft_offset[0],
            self.hitbox.y - self.hitbox_topleft_offset[1],
            Constants.TILESIZE,
            Constants.TILESIZE,
        )

    def draw(self, screen: pygame.Surface) -> None:
        if self.vel.magnitude() > 0.0:
            self.movement_state = EnemyMovementState.Running
        else:
            self.movement_state = EnemyMovementState.Idle
        screen.blit(
            self.sprite_sheet,
            self.drect,
            self.animations[self.direction + self.movement_state].frame(
                int(self.sprite_sheet.width / Constants.TILESIZE),
                Constants.TILESIZE,
            ),
        )

    def on_damage(self, damageAmt: int) -> None:
        self.curr_health -= damageAmt
        if self.curr_health <= 0:
            self.destroy()

    def get_hitbox(self) -> Rect:
        return self.hitbox


class Zombie(Enemy):

    img: pygame.Surface = None

    def __init__(self, x, y, speed=1, health=15):
        super().__init__(x, y, Vector2(0, 1), health=health)
        self.attack_power = 5
        if not Zombie.img:
            Zombie.img = utils.load_img(
                "assets/characters/Reptile/Reptile.png",
            )
        self.sprite_sheet = Zombie.img

    def load_sprite(self, sprite_path: str) -> None:
        self.sprite_sheet = pygame.image.load(sprite_path)

    def follow_player(self, player: Rect, dt: float) -> None:
        if player.x > self.drect.x:
            self.vel.x = self.zombie_speed
            self.direction = EnemyDirection.Right
        elif player.x < self.drect.x:
            self.vel.x = -self.zombie_speed
            self.direction = EnemyDirection.Left
        else:
            self.vel.x = 0

        if player.y > self.drect.y:
            self.vel.y = self.zombie_speed
            self.direction = EnemyDirection.Down
        elif player.y < self.drect.y:
            self.vel.y = -self.zombie_speed
            self.direction = EnemyDirection.Up
        else:
            self.vel.y = 0
