import pygame, sys
from settings import *
from random import choice, randint
from player import Player
from car import Car
from sprite import SimpleSprite, LongSprite



 # making our own class group so we can mod it for camera movement
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2() # creating an offset for our camera
        self.bg = pygame.image.load('../graphics/main/map.png').convert() # background
        self.fg = pygame.image.load('../graphics/main/overlay.png').convert_alpha() # foreground
    def customize_draw(self): #groups already have their own draw/sprite func, we are modding them 

        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2 # we are lookimng where our player is and 
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2 # moving the surfaces in the opposite direction


        display_surface.blit(self.bg,-self.offset) # display background first so everything is ontop

        # ordering the list using y pos so that we seem behind and infront of other img's 
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery ):
            offset_pos = sprite.rect.topleft - self.offset 
            display_surface.blit(sprite.image, offset_pos) # modding the group to display the images with
                                                           # the offset of our camera
        display_surface.blit(self.fg,-self.offset) # blit the foreground last so things go under 



pygame.init()

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

all_sprites = AllSprites() # naming the class group...this is normally all_sprites = pygame.sprite.Group()
obstical_sprites = pygame.sprite.Group() # creating a group to check for collisions that doesnt have the player in
player = Player((2062,3274),all_sprites,obstical_sprites)



# timer for cars
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 50)
pos_list = []

font = pygame.font.Font(None, 50)
text_surf = font.render('YOU HAVE WON!',True,'white')
text_rect = text_surf.get_rect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT/2))

music = pygame.mixer.Sound('../audio/music.mp3')
music.play(loops = -1)
crash = pygame.mixer.Sound('../audio/crash.mp3')
win_sound = pygame.mixer.Sound('../audio/win.mp3')

# sprite setup, we are importing the objects as sprites that we want collisions with
for file_name, pos_list in SIMPLE_OBJECTS.items(): # returns both key and value of dict
    path = f'../graphics/objects/simple/{file_name}.png' #add the key for the image
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list: # use the value to create its sprite
        SimpleSprite(surf,pos,[all_sprites,obstical_sprites])

for file_name, pos_list in LONG_OBJECTS.items(): # returns both key and value of dict
    path = f'../graphics/objects/long/{file_name}.png' #add the key for the image
    surf = pygame.image.load(path).convert_alpha()
    for pos in pos_list: # use the value to create its sprite
        LongSprite(surf,pos,[all_sprites,obstical_sprites])


while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == car_timer: # spawn a new car at timer interval
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list: # to make sure no cars spawn ontop of each other
                pos_list.append(random_pos)
                # this is just to offset the cars slightly to look more natural
                pos = (random_pos[0],random_pos[1] + randint(-8,8))
                #spawn a car at final pos
                Car(pos,[all_sprites,obstical_sprites])
            if len(pos_list) > 5: # so every 5th car could be spawned back at that position
                del pos_list[0]

    for sprite in player.collision_sprites.sprites():
        if sprite.hitbox.colliderect(player.hitbox):
            if hasattr(sprite,'name') and sprite.name == 'car':
                crash.play()
                player.kill()
                player = Player((2062,3274),all_sprites,obstical_sprites)


    

    delta_time = clock.tick() / 1000


    display_surface.fill('black')

    if player.pos.y >= 1180:
            
        # update
        all_sprites.update(delta_time) #need to pass in delta time for the other files to access it 


        all_sprites.customize_draw()
        # draw
        # all_sprites.draw(display_surface) <- this waould be oringinal way but we have modded the group
        
    else:
        all_sprites.update(delta_time)
        all_sprites.customize_draw()
        
        display_surface.blit(text_surf,text_rect)
        win_sound.play()
    

            

    


    pygame.display.update()



