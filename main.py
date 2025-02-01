import pygame
from tilemap import load_map


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    tilemap = load_map("assets/maps/map1.json")
    tileset_img = pygame.image.load("assets/tilesets/TilesetFloor.png")

    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill((120, 180, 255, 255))

        tilemap.draw(screen, tileset_img)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game()
