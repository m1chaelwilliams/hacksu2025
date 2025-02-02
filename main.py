import pygame
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes, load_img
from player import Player
from Enemy import Enemy, Zombie
from projectile import Projectile
from collisions import handle_collisons_one_to_many_x, handle_collisons_one_to_many_y
from itertools import filterfalse
from animation import Animation


class Entity:
    def __init__(self, rect):
        self.r = rect

    def get_hitbox(self):
        return self.r


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    tilemap = load_map("assets/maps/map1.json")
    tileset_floor_img_unscaled = pygame.image.load(
        "assets/tilesets/TilesetFloor.png",
    )
    tileset_trees_img_unscaled = pygame.image.load(
        "assets/tilesets/TilesetNature.png",
    )
    tileset_trees_img = pygame.transform.scale_by(
        tileset_trees_img_unscaled,
        Constants.TILESIZE / Constants.IMPORT_TILESIZE,
    )
    tileset_floor_img = pygame.transform.scale_by(
        tileset_floor_img_unscaled,
        Constants.TILESIZE / Constants.IMPORT_TILESIZE,
    )

    shuriken_img = load_img("assets/weapons/shuriken/shuriken.png")

    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (
            Constants.TILESIZE * 2 - 10,
            Constants.TILESIZE * 2 - 10,
        ),
        (5, 5),
    )
    trees = []
    for rect in tree_rects:
        trees.append(Entity(rect))

    clock = pygame.time.Clock()

    player = Player([], (14.5, 9.5))
    projectiles: list[Projectile] = []

    zombie = Zombie(100, 100, 50, 50, speed=200)
    running = True
    dt = 0.0

    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (Constants.TILESIZE * 2 - 10, Constants.TILESIZE * 2 - 10),
        (5, 5),
    )

    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running = False

        player.update(events)
        if player.attacking:
            player.attacking = False
            mouse_pos = pygame.mouse.get_pos()
            proj_vec = pygame.math.Vector2(
                mouse_pos[0] - player.drect.center[0],
                mouse_pos[1] - player.drect.center[1],
            ).normalize()
            projectiles.append(
                Projectile(
                    (player.drect.x, player.drect.y),
                    proj_vec,
                    1000,
                    shuriken_img,
                    Animation(0, 1, 0.08),
                )
            )

        player.move_x(dt)
        player.hitbox = handle_collisons_one_to_many_x(
            player.hitbox,
            player.vel,
            trees,
        )
        player.update_drect_from_hitbox()

        player.move_y(dt)
        player.hitbox = handle_collisons_one_to_many_y(
            player.hitbox,
            player.vel,
            trees,
        )

        player.update_drect_from_hitbox()

        for projectile in projectiles:
            projectile.update(dt)
            projectile.move_x(dt)
            projectile.move_y(dt)
        projectiles = list(filterfalse(lambda p: not p.alive, projectiles))

        screen.fill((120, 180, 255, 255))

        tilemap.draw_layer(
            0,
            screen,
            tileset_floor_img,
            sprite_size=(Constants.TILESIZE, Constants.TILESIZE),
            tileset_width_in_tiles=22,
        )
        tilemap.draw_layer(
            1,
            screen,
            tileset_trees_img,
            sprite_size=(Constants.TILESIZE * 2, Constants.TILESIZE * 2),
            tileset_width_in_tiles=12,
        )
        player.draw(screen)

        zombie.follow_player(player.hitbox, dt)  # Set velocity
        zombie.move_x(dt)  # Apply velocity to position
        zombie.draw(screen)  # Draw enemy

        # for enemie in enemies:
        #   enemie.draw(screen)

        for projectile in projectiles:
            projectile.draw(screen)

        for rect in trees:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                rect.get_hitbox(),
                1,
            )

        pygame.draw.rect(
            screen,
            (0, 255, 0),
            player.hitbox,
            1,
        )
        pygame.draw.rect(
            screen,
            (0, 0, 255),
            player.drect,
            1,
        )

        # screen.blit(player_img, pos, pygame.rect.Rect(0, 0, 16, 16))

        pygame.display.update()

        dt = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    game()
