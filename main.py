import pygame
from pygame import Rect
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes, load_img
from player import Player
from Enemy import Zombie, Gladiator, Robot
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

    shuriken_img = load_img("assets/weapons/shuriken/shuriken.png")

    tree_rects = get_hitboxes(
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

    player = Player([], (Constants.WINDOW_WIDTH / 2.0, Constants.WINDOW_HEIGHT / 2.0))
    projectiles: list[Projectile] = []
    enemy_projectiles: list[Projectile] = []

    enemies = []
    running = True
    dt = 0.0

    font = pygame.font.Font(None, 36)
    timer = 0
    wave = 1
    last_time_update = pygame.time.get_ticks()

    mixer.music.load("assets/music/doom.mp3")
    mixer.music.play(loops=100)
    sounds: dict[str, pygame.Sound] = {
        "hit": pygame.Sound("assets/sfx/Hit.wav"),
    }

    num_enemies_to_spawn = 2
    num_enemies_spawned = 0
    enemy_spawn_rate = 2.0
    enemy_spawn_duration_left = enemy_spawn_rate
    spawning_enemies = True

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

        if spawning_enemies:
            enemy_spawn_duration_left -= dt
            if enemy_spawn_duration_left <= 0.0:
                num_enemies_spawned += 1
                if num_enemies_spawned == num_enemies_to_spawn:
                    spawning_enemies = False
                    num_enemies_to_spawn *= 2
                enemy_spawn_duration_left = enemy_spawn_rate
                location = SpawnLoc.random_spawn_side()
                enemy_choice = random.randint(wave - 3, wave - 1)
                enemy_choice = max(0, enemy_choice)
                if enemy_choice == 0:
                    enemies.append(
                        Zombie(
                            location[0],
                            location[1],
                        )
                    )
                elif enemy_choice == 1:
                    enemies.append(
                        Gladiator(
                            location[0],
                            location[1],
                        )
                    )
                else:
                    enemies.append(Robot(location[0], location[1]))
            pass

        if not spawning_enemies and len(enemies) == 0:
            num_enemies_spawned = 0
            spawning_enemies = True
            wave += 1
            enemy_spawn_rate *= 0.9

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
                if projectile.hitbox.colliderect(player.get_hitbox()):
                    sounds["hit"].play()
                    projectile.alive = False
                    player.health -= projectile.damage
                    if player.health < 0:
                        print("you died!")
                        running = False

                for tree in trees:
                    if projectile.hitbox.colliderect(tree.get_hitbox()):
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
                    if enemy.get_hitbox().colliderect(projectile.hitbox):
                        projectile.alive = False
                        sounds["hit"].play()
                        enemy.curr_health -= projectile.damage
                        if enemy.curr_health <= 0.0:
                            enemy.alive = False
                            killed_enemy = True
                if killed_enemy:
                    enemies = list(filterfalse(lambda p: not p.alive, enemies))

                for tree in trees:
                    if projectile.hitbox.colliderect(tree.get_hitbox()):
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

        for projectile in projectiles:
            projectile.draw(screen)
        for projectile in enemy_projectiles:
            projectile.draw(screen)

        draw_player_ui(screen, imgs, player)

        timer_text = font.render(f"Elapsed time: {timer}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 600))

        wave_text = font.render(f"Wave: {wave}", True, (255, 255, 255))
        screen_size = pygame.display.get_window_size()
        screen.blit(wave_text, ((screen_size[0] - wave_text.width) / 2, 0.0))
        # print(timer)
        pygame.display.update()

        dt = clock.tick(60) / 1000.0

    pygame.quit()


if __name__ == "__main__":
    game()
