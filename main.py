import pygame
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes
from player import Player


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    tilemap = load_map("assets/maps/map1.json")
    tileset_img = pygame.image.load("assets/tilesets/TilesetFloor.png")

    clock = pygame.time.Clock()

    player = Player([], (0, 0))

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

        player.move_x(dt)

        for rect in tree_rects:
            if player.hitbox.colliderect(rect):
                if player.vel.x > 0:
                    player.hitbox.right = rect.left
                else:
                    player.hitbox.left = rect.right
                player.update_drect_from_hitbox()

        player.move_y(dt)

        for rect in tree_rects:
            if player.hitbox.colliderect(rect):
                if player.vel.y > 0:
                    player.hitbox.bottom = rect.top
                else:
                    player.hitbox.top = rect.bottom
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
        # foo = 1
        # print(f"foo is {foo}", )

    pygame.quit()


if __name__ == "__main__":
    game()
