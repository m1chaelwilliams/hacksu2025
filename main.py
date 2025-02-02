import pygame
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes
from player import Player
from Enemy import Enemy, Zombie
from collisions import handle_collisons_one_to_many_x, handle_collisons_one_to_many_y


class Entity:
    def __init__(self, rect):
        self.r = rect

    def get_hitbox(self):
        return self.r

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280

def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    tilemap = load_map("assets/maps/map1.json")
    tileset_floor_img = pygame.image.load("assets/tilesets/TilesetFloor.png")
    tileset_trees_img = pygame.image.load("assets/tilesets/TilesetNature.png")
    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (Constants.TILESIZE * 2 - 10, Constants.TILESIZE * 2 - 10),
        (5, 5),
    )
    trees = []
    for rect in tree_rects:
        trees.append(Entity(rect))

    clock = pygame.time.Clock()

    player = Player([], (0, 0))

    zombie = Zombie(100, 100, 50, 50, speed = 2)
    running = True
    dt = 0.0

    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (Constants.TILESIZE * 2 - 10, Constants.TILESIZE * 2 - 10),
        (5, 5),
    )

    tileset_floor_img = pygame.image.load("assets/tilesets/TilesetFloor.png")
    tileset_trees_img = pygame.image.load("assets/tilesets/TilesetNature.png")
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    running = False

        player.update()

        zombie.draw(screen)
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

        screen.fill((120, 180, 255, 255))

        tilemap.draw_layer(0, screen, tileset_floor_img)
        tilemap.draw_layer(
            1,
            screen,
            tileset_trees_img,
            sprite_size=(Constants.TILESIZE * 2, Constants.TILESIZE * 2),
            tileset_width_in_tiles=12,
        )
        player.draw(screen)

        for rect in tree_rects:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                rect,
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
        
        print("tick " + str(pygame.time.get_ticks()))
        clock.tick(60)


    pygame.quit()


if __name__ == "__main__":
    game()
