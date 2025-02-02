import pygame
from tilemap import load_map


def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    
    tilemap = load_map("assets/maps/map1.json")
    tileset_img = pygame.image.load("assets/tilesets/TilesetFloor.png")

    img = pygame.image.load("assets/ninja_adventure/Actor/Animals/Fish/FacesetRed.png")
    
    clock = pygame.time.Clock()
    
    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        

        screen.fill((120, 180, 255, 255))

        tilemap.draw(screen, tileset_img)
        
        pygame.display.update()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            img.y -= 300
        if keys[pygame.K_s]:
            img.y += 300
        if keys[pygame.K_a]:
            img.x -= 300
        if keys[pygame.K_d]:
            img.x += 300

        #print("tick " + str(pygame.time.get_ticks()))
        clock.tick(60)
        # foo = 1
        # print(f"foo is {foo}", )

    pygame.quit()


if __name__ == "__main__":
    game()