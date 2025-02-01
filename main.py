import pygame
from constants import Constants
from tilemap import load_map
from utils import get_hitboxes


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    tilemap = load_map("assets/maps/map1.json")
    tileset_floor_img = pygame.image.load("assets/tilesets/TilesetFloor.png")
    tileset_trees_img = pygame.image.load("assets/tilesets/TilesetNature.png")
    tree_rects = get_hitboxes(
        0,
        tilemap.layers[1],
        (Constants.TILESIZE * 2 - 10, Constants.TILESIZE * 2 - 10),
        (5, 5),
    )

    clock = pygame.time.Clock()

    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill((120, 180, 255, 255))

        tilemap.draw_layer(0, screen, tileset_floor_img)
        tilemap.draw_layer(
            1,
            screen,
            tileset_trees_img,
            sprite_size=(Constants.TILESIZE * 2, Constants.TILESIZE * 2),
            tileset_width_in_tiles=12,
        )

        for rect in tree_rects:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                rect,
                1,
            )

        # screen.blit(player_img, pos, pygame.rect.Rect(0, 0, 16, 16))

        pygame.display.update()
        # print("tick " + str(pygame.time.get_ticks()))
        clock.tick(60)
        # foo = 1
        # print(f"foo is {foo}", )

    pygame.quit()


if __name__ == "__main__":
    game()
