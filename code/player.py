import pygame, sys
from os import walk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        self.import_assets()
        self.frame_index = 0 # a way to pick each frame to add into the self.image then update image
        self.status = 'down' # can change this in input to change the dict[key] 
        self.image = self.animations[self.status][self.frame_index] # dict we created to select the images 
        
        self.rect = self.image.get_rect(center = pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200

        #collisions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.inflate(-35, -self.rect.height / 2)

    def collisions(self, direction):
     
        if direction == 'horizontal':
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    
                    if self.direction.x > 0: # checking if we are moving right against the left side of a rect
                        self.hitbox.right = sprite.hitbox.left # bumping into rect
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx # we need to update our rect to new position
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx
        else:
                    
            for sprite in self.collision_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
    
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery 
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery 
  
    def import_assets(self):

        # this is one way to add the images if only have a small amount 
        # path = "../graphics/player/right/"  
        # self.animation = [pygame.image.load(f'{path}{frame}.png').convert_alpha() for frame in range(4)]

        # this is another way to do it
        # for frame in range(4): 
        #     surf = pygame.image.load(f'{path}{frame}.png').convert_alpha()
        #     self.animation.append(surf)

        self.animations = {} # a dictionary for us to add a list of images to a key of up,down,left,right
        # enumerate numbers the items and returns a tuple that we can asign variables to both
        for index, folder in enumerate(walk('../graphics/player')):
            if index == 0:
                for name in folder[1]: # walk returns a list of path then folders then files 
                    self.animations[name] = []
            else:
                for file_name in folder[2]:
                    path = folder[0].replace('\\','/') + '/' + file_name # change backslash for python
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1] # finding the right key word for dictionary to add the path for image
                    self.animations[key].append(surf)

    def move(self,delta_time):

        # because our vector makes you travel faster in the diagonal besause x + 1 and y + 1 is 1.4 diagonally
        # we have to normalize our vectors using this method .but only when the movement isnt zero because
        # python cant normalize 0,0.....magnitude() is just the length if the vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # we are splitting the movement for collisions
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * delta_time
        self.hitbox.centerx = round(self.pos.x) # update the smaller hitbox first to be more accurate
        self.rect.centerx = self.hitbox.centerx # then update the image rect
        self.collisions('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * delta_time
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collisions('vertical')
        
    def input(self):
        
        keys = pygame.key.get_pressed() # return a list of all booleans foe every key
        
        if keys[pygame.K_UP]: # checking boolean for keys for vertical movement
            self.direction.y = - 1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = + 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]: # horizontal movement
            self.direction.x = + 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = - 1
            self.status = 'left'
        else:
            self.direction.x = 0

    def animate(self,delta_time):
        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0: # so that the caracter animation is 0 when not moving
            self.frame_index += 10 * delta_time # returns a float for movement as usual
            if self.frame_index >= len(current_animation): # makes sure we restart animation if all frames are used
                self.frame_index = 0
        else:
            self.frame_index = 0
        self.image = current_animation[int(self.frame_index)] # converts float into integer for frame choice

    def restrict(self):
        if self.rect.left < 640:
            self.pos.x = 640 + self.rect.width / 2
            self.hitbox.left = 640
            self.rect.left = 640

        if self.rect.right > 2560:
            self.pos.x = 2560 - self.rect.width / 2
            self.hitbox.right = 2560
            self.rect.right = 2560

        if self.rect.bottom > 3500:
            self.pos.y = 3500 - self.rect.height / 2
            self.rect.bottom = 3500
            self.hitbox.centery = self.rect.centery

        if self.rect.top < 1180:
            self.pos.y = 1180 - self.rect.height /2
            self.rect.top = 1180
            self.hitbox.centery = self.rect.centery

    def update(self,delta_time):
        self.input()
        self.move(delta_time)
        self.animate(delta_time)
        self.restrict()




