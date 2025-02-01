import pygame


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))

    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill((120, 180, 255, 255))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    game()
