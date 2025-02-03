import pygame
from pygame import Rect
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes, load_img
from player import Player
from Enemy import Zombie, Gladiator
from projectile import Projectile
from collisions import handle_collisons_one_to_many_x, handle_collisons_one_to_many_y
from itertools import filterfalse
from animation import Animation
import pygame.mixer as mixer
from spawn import SpawnLoc
import random


class Entity:
    def __init__(self, rect):
        self.r = rect

    def get_hitbox(self):
        return self.r



def draw_player_ui(
    screen: pygame.Surface,
    imgs: dict[str, pygame.Surface],
    player: Player,
) -> None:
    cur_x = 0
    for i in range(player.health):
        screen.blit(
            imgs["heart"],
            (cur_x, 0),
            Rect(
                Constants.TILESIZE * 4,
                0,
                Constants.TILESIZE,
                Constants.TILESIZE,
            ),
        )
        cur_x += Constants.TILESIZE




def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
    tilemap = load_map("assets/maps/map1.json")
    imgs: dict[str, pygame.Surface] = {
        "heart": load_img("assets/ui/heart.png"),
        "tileset_floor": load_img("assets/tilesets/TilesetFloor.png"),
        "tileset_trees": load_img("assets/tilesets/TilesetNature.png"),
        "shuriken": load_img("assets/weapons/shuriken/shuriken.png"),
    }

    # tileset_floor_img_unscaled = pygame.image.load(
    #     "assets/tilesets/TilesetFloor.png",
    # )
    # tileset_trees_img_unscaled = pygame.image.load(
    #     "assets/tilesets/TilesetNature.png",
    # )
    # tileset_trees_img = pygame.transform.scale_by(
    #     tileset_trees_img_unscaled,
    #     Constants.TILESIZE / Constants.IMPORT_TILESIZE,
    # )
    # tileset_floor_img = pygame.transform.scale_by(
    #     tileset_floor_img_unscaled,
    #     Constants.TILESIZE / Constants.IMPORT_TILESIZE,
    # )

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
    enemy_projectiles: list[Projectile] = []

    enemies = []
    for i in range(2):
        location = SpawnLoc.random_spawn_side()
        enemies.append(
            Zombie(
                location[0],
                location[1],
            ),
        )
        location2 = SpawnLoc.random_spawn_side()
        enemies.append(
            Gladiator(
                location2[0],
                location2[1],
            ),
        )

    running = True
    dt = 0.0

    font = pygame.font.Font(None, 36) 
    last_time_update = pygame.time.get_ticks() 
    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (Constants.TILESIZE * 2 - 10, Constants.TILESIZE * 2 - 10),
        (5, 5),
    )

    mixer.music.load("assets/music/doom.mp3")
    mixer.music.play(loops=100)
    sounds: dict[str, pygame.Sound] = {
        "hit": pygame.Sound("assets/sfx/Hit.wav"),
    }

    timer = 0
    wave_interval = 15000

    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running = False



        current_time = pygame.time.get_ticks()
        if current_time - last_time_update >= 1000:  
            timer += 1
            last_time_update = current_time
        print(f"Current Time: current time: {current_time}")
        

        if current_time == wave_interval:

            for i in range(random.randint(10,20)):
                location = SpawnLoc.random_spawn_side()
                enemies.append(
                    Zombie(
                        location[0],
                        location[1],
                    ),
                )
                location2 = SpawnLoc.random_spawn_side()
                enemies.append(
                    Gladiator(
                        location2[0],
                        location2[1],
                    ),
                )


        player.update(dt, events)
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

        for projectile in enemy_projectiles:
            projectile.update(dt)
            projectile.move_x(dt)
            projectile.move_y(dt)

            if projectile.alive:
                if projectile.drect.colliderect(player.get_hitbox()):
                    sounds["hit"].play()
                    projectile.alive = False
                    player.health -= projectile.damage
                    if player.health < 0:
                        print("you died!")
                        running = False

                for tree in trees:
                    if projectile.drect.colliderect(tree.get_hitbox()):
                        projectile.alive = False
                        sounds["hit"].play()
        enemy_projectiles = list(filterfalse(lambda p: not p.alive, enemy_projectiles))

        for projectile in projectiles:
            projectile.update(dt)
            projectile.move_x(dt)
            projectile.move_y(dt)

            if projectile.alive:

                killed_enemy = False
                for enemy in enemies:
                    if enemy.get_hitbox().colliderect(projectile.drect):
                        projectile.alive = False
                        sounds["hit"].play()
                        enemy.curr_health -= projectile.damage
                        if enemy.curr_health <= 0.0:
                            enemy.alive = False
                            killed_enemy = True
                if killed_enemy:
                    enemies = list(filterfalse(lambda p: not p.alive, enemies))

                for tree in trees:
                    if projectile.drect.colliderect(tree.get_hitbox()):
                        projectile.alive = False
                        sounds["hit"].play()
        projectiles = list(filterfalse(lambda p: not p.alive, projectiles))

        screen.fill((120, 180, 255, 255))

        tilemap.draw_layer(
            0,
            screen,
            imgs["tileset_floor"],
            sprite_size=(Constants.TILESIZE, Constants.TILESIZE),
            tileset_width_in_tiles=22,
        )
        tilemap.draw_layer(
            1,
            screen,
            imgs["tileset_trees"],
            sprite_size=(Constants.TILESIZE * 2, Constants.TILESIZE * 2),
            tileset_width_in_tiles=12,
        )
        player.draw(screen)

        hit_player = False
        for enemy in enemies:
            enemy.update(dt, events)
            enemy.follow_player(player.drect, dt)
            enemy.move_x(dt)
            enemy.move_y(dt)
            if not hit_player and player.attacked_cooldown <= 0.0:
                if enemy.wants_attack:
                    enemy.attack(player, enemy_projectiles, imgs)
                if enemy.get_hitbox().colliderect(player.get_hitbox()):
                    hit_player = True
                    player.health -= enemy.attack_power
                    player.vel += enemy.vel * 50  # knockback player
                    player.attacked_cooldown = Player.attacked_cooldown
                    if player.health <= 0:
                        print("you died")
                        running = False

            enemy.draw(screen)

        # for enemie in enemies:
        #   enemie.draw(screen)

        for projectile in projectiles:
            projectile.draw(screen)
        for projectile in enemy_projectiles:
            projectile.draw(screen)

        for rect in trees:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                rect.get_hitbox(),
                1,
            )

        # pygame.draw.rect(
        #     screen,
        #     (0, 255, 0),
        #     player.hitbox,
        #     1,
        # )
        # pygame.draw.rect(
        #     screen,
        #     (0, 0, 255),
        #     player.drect,
        #     1,
        # )
        #
        # screen.blit(player_img, pos, pygame.rect.Rect(0, 0, 16, 16))

        draw_player_ui(screen, imgs, player)

        timer_text = font.render(f"Next Wave: {timer}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 600))
        pygame.display.update()
        dt = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    game()