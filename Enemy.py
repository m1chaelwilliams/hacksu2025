import pygame
from pygame.rect import Rect
from pygame.math import Vector2
from constants import Constants
import random
import utils
from animation import Animation
from projectile import Projectile


class EnemyMovementState:
    Idle = 10
    Running = 20


class EnemyDirection:
    Left = 0
    Right = 1
    Up = 2
    Down = 3


class Enemy(pygame.sprite.Sprite):
    speed = 100

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
        self.wants_attack = False
        self.attack_cooldown = 1.0

    def update(self, dt: float, events: list[pygame.event.Event]) -> None:
        self.animations[self.direction + self.movement_state].update(dt)

    def attack(self, player, proj_list, imgs) -> None:
        pass

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
    starting_health = 3
    speed = 60

    def __init__(self, x, y):
        super().__init__(x, y, Vector2(0, 1), health=Zombie.starting_health)
        self.attack_power = 1
        if not Zombie.img:
            Zombie.img = utils.load_img(
                "assets/characters/Reptile/Reptile.png",
            )
        self.sprite_sheet = Zombie.img
        self.speed = Zombie.speed

    def follow_player(self, player: Rect, dt: float) -> None:
        if player.x > self.drect.x:
            self.vel.x = self.speed
            self.direction = EnemyDirection.Right
        elif player.x < self.drect.x:
            self.vel.x = -self.speed
            self.direction = EnemyDirection.Left
        else:
            self.vel.x = 0

        if player.y > self.drect.y:
            self.vel.y = self.speed
            self.direction = EnemyDirection.Down
        elif player.y < self.drect.y:
            self.vel.y = -self.speed
            self.direction = EnemyDirection.Up
        else:
            self.vel.y = 0


class Gladiator(Enemy):

    img: pygame.Surface = None
    ideal_player_distance = Constants.TILESIZE * 3
    starting_health = 5
    speed = 100
    attack_power = 2
    attack_cooldown = 2

    def __init__(self, x, y):
        super().__init__(x, y, Vector2(0, 1), health=Gladiator.starting_health)
        self.attack_power = Gladiator.attack_power
        if not Gladiator.img:
            Gladiator.img = utils.load_img(
                "assets/characters/GladiatorBlue/SpriteSheet.png",
            )
        self.sprite_sheet = Gladiator.img
        self.speed = Gladiator.speed
        self.attack_power = Gladiator.attack_power
        self.attack_cooldown = Gladiator.attack_cooldown

    def follow_player(self, player: Rect, dt: float) -> None:
        self.attack_cooldown -= dt
        self.vel = Vector2(0, 0)

        if player.x > self.drect.x:
            self.vel.x = self.speed
            self.direction = EnemyDirection.Right
        elif player.x < self.drect.x:
            self.vel.x = -self.speed
            self.direction = EnemyDirection.Left

        if player.y > self.drect.y:
            self.vel.y = self.speed
            self.direction = EnemyDirection.Down
        elif player.y < self.drect.y:
            self.vel.y = -self.speed
            self.direction = EnemyDirection.Up

        if (
            Vector2(self.drect.x, self.drect.y).distance_to(Vector2(player.x, player.y))
            < Gladiator.ideal_player_distance * 2
        ):
            if self.attack_cooldown <= 0.0:
                self.wants_attack = True

    def attack(self, player, proj_list, imgs) -> None:
        self.wants_attack = False
        self.attack_cooldown = Gladiator.attack_cooldown
        proj_list.append(
            Projectile(
                (self.drect.center[0], self.drect.center[1]),
                Vector2(
                    player.get_hitbox().center[0] - self.hitbox.center[0],
                    player.get_hitbox().center[1] - self.hitbox.center[1],
                ).normalize(),
                1000,
                imgs["shuriken"],
                Animation(
                    0,
                    1,
                    0.8,
                ),
            )
        )

    # IDEA: fast but low hp. has dashes?
    class Wolf:
        def follow_player(self, player: Rect, dt: float) -> None:
            self.attack_cooldown -= dt

            if player.x > self.drect.x + Gladiator.ideal_player_distance:
                self.vel.x = self.speed
                self.direction = EnemyDirection.Right
            elif player.x < self.drect.x - Gladiator.ideal_player_distance:
                self.vel.x = -self.speed
                self.direction = EnemyDirection.Left
            else:
                self.vel.x = 0

            if player.y > self.drect.y + Gladiator.ideal_player_distance:
                self.vel.y = self.speed
                self.direction = EnemyDirection.Down
            elif player.y < self.drect.y - Gladiator.ideal_player_distance:
                self.vel.y = -self.speed
                self.direction = EnemyDirection.Up
            else:
                self.vel.y = 0


class Robot(Enemy):
    img: pygame.Surface = None
    ideal_player_distance = Constants.TILESIZE * 3
    starting_health = 5
    speed = 100.0
    attack_power = 1
    attack_cooldown = 2

    def __init__(self, x, y):
        super().__init__(x, y, Vector2(0, 1), health=Gladiator.starting_health)
        self.attack_power = Robot.attack_power
        if not Robot.img:
            Robot.img = utils.load_img(
                "assets/characters/RobotCamouflage/SpriteSheet.png",
            )
        self.sprite_sheet = Robot.img
        self.speed = Robot.speed
        self.attack_power = Robot.attack_power
        self.attack_cooldown = Robot.attack_cooldown

    def follow_player(self, player: Rect, dt: float) -> None:
        self.attack_cooldown -= dt

        if player.x > self.drect.x + Gladiator.ideal_player_distance:
            self.vel.x = self.speed
            self.direction = EnemyDirection.Right
        elif player.x < self.drect.x - Gladiator.ideal_player_distance:
            self.vel.x = -self.speed
            self.direction = EnemyDirection.Left
        else:
            self.vel.x = 0

        if player.y > self.drect.y + Gladiator.ideal_player_distance:
            self.vel.y = self.speed
            self.direction = EnemyDirection.Down
        elif player.y < self.drect.y - Gladiator.ideal_player_distance:
            self.vel.y = -self.speed
            self.direction = EnemyDirection.Up
        else:
            self.vel.y = 0

        if (
            Vector2(self.drect.x, self.drect.y).distance_to(Vector2(player.x, player.y))
            < Gladiator.ideal_player_distance * 2
        ):
            if self.attack_cooldown <= 0.0:
                self.wants_attack = True

    def spawn_proj(
        self,
        img: pygame.Surface,
        proj_list,
        pos: tuple[int, int],
        dir: tuple[int, int],
    ) -> None:
        proj_list.append(
            Projectile(
                pos,
                Vector2(
                    dir[0],
                    dir[1],
                ).normalize(),
                1000,
                img,
                Animation(
                    0,
                    1,
                    0.8,
                ),
            )
        )

    def attack(self, player, proj_list, imgs) -> None:
        self.wants_attack = False
        self.attack_cooldown = Gladiator.attack_cooldown
        self.spawn_proj(imgs["shuriken"], proj_list, self.drect.center, (1, 0))
        self.spawn_proj(imgs["shuriken"], proj_list, self.drect.center, (0, 1))
        self.spawn_proj(imgs["shuriken"], proj_list, self.drect.center, (-1, 0))
        self.spawn_proj(imgs["shuriken"], proj_list, self.drect.center, (0, -1))
        # proj_list.append(
        #     Projectile(
        #         (self.drect.center[0], self.drect.center[1]),
        #         Vector2(
        #             1,
        #             0,
        #         ).normalize(),
        #         1000,
        #         imgs["shuriken"],
        #         Animation(
        #             0,
        #             1,
        #             0.8,
        #         ),
        #     )
        # )

    # IDEA: fast but low hp. has dashes?
    class Wolf:
        def follow_player(self, player: Rect, dt: float) -> None:
            self.attack_cooldown -= dt

            if player.x > self.drect.x + Gladiator.ideal_player_distance:
                self.vel.x = self.speed
                self.direction = EnemyDirection.Right
            elif player.x < self.drect.x - Gladiator.ideal_player_distance:
                self.vel.x = -self.speed
                self.direction = EnemyDirection.Left
            else:
                self.vel.x = 0

            if player.y > self.drect.y + Gladiator.ideal_player_distance:
                self.vel.y = self.speed
                self.direction = EnemyDirection.Down
            elif player.y < self.drect.y - Gladiator.ideal_player_distance:
                self.vel.y = -self.speed
                self.direction = EnemyDirection.Up
            else:
                self.vel.y = 0
