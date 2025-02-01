import pygame
from dataclasses import dataclass

class Sprite:
    health = 5
    color = (120, 180, 255, 255)



def game() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    
    clock = pygame.time.Clock()
    
    img = pygame.image.load("assets/ninja_adventure/Actor/Characters/Pig/SeparateAnim/Idle.png").convert()
    img = pygame.transform.scale(img, (1280, 720))
    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        

        screen.fill((120, 180, 255, 255))
        screen.blit(img,(0,0))
        pygame.display.update()
        
        print("tick " + str(pygame.time.get_ticks()))
        clock.tick(60)
        # foo = 1
        # print(f"foo is {foo}", )

    pygame.quit()


if __name__ == "__main__":
    game()