import pygame
from pygame.rect import Rect
from pygame.math import Vector2
from constants import Constants
from animation import Animation
import utils


class PlayerMovementState:
    Idle = 10
    Running = 20


class PlayerDirection:
    Left = 0
    Right = 1
    Up = 2
    Down = 3


class Player(pygame.sprite.Sprite):

    speed = 200
    
    def __init__(self, groups, init_pos: tuple[int, int]):
        self.attacking = False
        self.sprite_sheet = utils.load_img(
            "assets/characters/NinjaDark/SpriteSheet.png"
        )
        self.sprite_sheet_num_tiles_per_row = int(
            self.sprite_sheet.width / Constants.TILESIZE
        )
        self.animations: dict[int, Animation] = {
            PlayerDirection.Down + PlayerMovementState.Idle: Animation(0, 1, 100),
            PlayerDirection.Up + PlayerMovementState.Idle: Animation(1, 2, 100),
            PlayerDirection.Left + PlayerMovementState.Idle: Animation(2, 3, 100),
            PlayerDirection.Right + PlayerMovementState.Idle: Animation(3, 4, 100),
            PlayerDirection.Down
            + PlayerMovementState.Running: Animation(4, 16, 0.1, 4),
            PlayerDirection.Up + PlayerMovementState.Running: Animation(5, 17, 0.1, 4),
            PlayerDirection.Left
            + PlayerMovementState.Running: Animation(6, 18, 0.1, 4),
            PlayerDirection.Right
            + PlayerMovementState.Running: Animation(7, 19, 0.1, 4),
        }
        self.direction: PlayerDirection = PlayerDirection.Down
        self.movement_state: PlayerMovementState = PlayerMovementState.Idle

        self.srect = Rect(
            0,
            0,
            Constants.TILESIZE,
            Constants.TILESIZE,
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

    def update(self, dt: float, events: list[pygame.event.Event]) -> None:
        self.vel.x = 0
        self.vel.y = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.vel.y = -Player.speed
            self.direction = PlayerDirection.Up
        if keys[pygame.K_a]:
            self.vel.x = -Player.speed
            self.direction = PlayerDirection.Left
        if keys[pygame.K_s]:
            self.vel.y = Player.speed
            self.direction = PlayerDirection.Down
        if keys[pygame.K_d]:
            self.vel.x = Player.speed
            self.direction = PlayerDirection.Right

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.attacking = True

        self.animations[self.direction + self.movement_state].update(dt)
        #normalize
        if self.vel.length() > Player.speed:
            self.vel.normalize_ip() 
            self.vel *= Player.speed 

    def draw(self, screen: pygame.Surface) -> None:
        if self.vel.magnitude() > 0.0:
            self.movement_state = PlayerMovementState.Running
        else:
            self.movement_state = PlayerMovementState.Idle
        screen.blit(
            self.sprite_sheet,
            self.drect,
            self.animations[self.direction + self.movement_state].frame(
                self.sprite_sheet_num_tiles_per_row,
                Constants.TILESIZE,
            ),
        )

    def collides(self, rect: Rect) -> bool:
        return self.hitbox.colliderect(rect)

    def move_x(self, dt: float) -> None:
        self.drect.x += self.vel.x * dt
        self.hitbox.x += self.vel.x * dt
        self.clamp_on_edge(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)

    def move_y(self, dt: float) -> None:
        self.drect.y += self.vel.y * dt
        self.hitbox.y += self.vel.y * dt
        self.clamp_on_edge(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)

    def clamp_on_edge(self, screen_width: int, screen_height: int) -> None:
        if self.drect.left < 0:
            self.drect.left = 0
            self.vel.x = 0
        if self.drect.right > screen_width:
            self.drect.right = screen_width
            self.vel.x = 0
        if self.drect.top < 0:
            self.drect.top = 0
            self.vel.y = 0
        if self.drect.bottom > screen_height:
            self.drect.bottom = screen_height
            self.vel.y = 0

        # Keep hitbox aligned with drect
        self.hitbox.x = self.drect.x + self.hitbox_topleft_offset[0]
        self.hitbox.y = self.drect.y + self.hitbox_topleft_offset[1]

    def get_hitbox(self) -> Rect:
        return self.hitbox

    def update_drect_from_hitbox(self) -> None:
        self.drect = Rect(
            self.hitbox.x - self.hitbox_topleft_offset[0],
            self.hitbox.y - self.hitbox_topleft_offset[1],
            Constants.TILESIZE,
            Constants.TILESIZE,
        )
