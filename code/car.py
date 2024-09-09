import pygame
from random import choice
from os import walk


class Car(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.name = 'car'

        for _, _, img_list in walk('../graphics/cars'): # just to find a random image using walk
            car_name = choice(img_list)
        
        self.image = pygame.image.load('../graphics/cars/' + car_name).convert_alpha() # insert the random choice
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, -self.rect.height / 2)

        self.pos = pygame.math.Vector2(self.rect.center)

        if pos[0] < 200:
            self.direction = pygame.math.Vector2(1,0) # just changing the direction of the car depending on which side it spawned
        else:
            self.direction = pygame.math.Vector2(-1,0)
            self.image = pygame.transform.flip(self.image,True,False) # flipping the image if it is moving left

        self.speed = 300

    def update(self,delta_time):
        self.pos += self.direction * self.speed * delta_time
        self.hitbox.center = (round(self.pos.x),round(self.pos.y))
        self.rect.center = self.hitbox.center

        if not -200 < self.rect.x < 3400: # these numbers are the size of the map 
            self.kill()

    

       


