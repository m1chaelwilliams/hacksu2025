import pygame
from pygame.rect import Rect

from pygame.math import Vector2



class Enemy:

    def __init__(self, x: int, 
                y: int, 
                width: int, 
                height: int, 
                direction: Vector2 = Vector2(0, 1), 
                speed: int = 1,
                health: int = 10
                ):
        self.direction = direction 
        self.velocity = 0

        self.hitbox = Rect(x, y, width, height) 
        self.speed = speed 
        self.max_health = health
        self.curr_health = health

    def destroy(self):
        print("destroy")    

    def x_move(self):
        self.hitbox.x += self.direction.x * self.speed

    def y_move(self):
        self.hitbox.y += self.direction.y * self.speed



    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox) 

    def damage(self, damageAmt):
        curr_health -= damageAmt
        if curr_health <= 0:
            self.destroy()
        

class Zombie(Enemy):

    def __init__(self, x, y, width, height, speed=1, health=15):
        super().__init__(x, y, width, height, Vector2(0, 1), speed, health)
        self.sprite = None 
        self.attack_power = 5 

    def load_sprite(self, sprite_path):
        self.sprite = pygame.image.load(sprite_path)

    