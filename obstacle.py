
import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type): # ['fly','fly','snail']
        super().__init__() # runs the father object init function

        if type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300
            self.x_speed = 2
            self.type = type
        
        elif type == 'husk':
            husk = pygame.transform.scale(pygame.image.load('graphics/husk/husk.png').convert_alpha(),(70,70))
            husk_2 = pygame.transform.scale(pygame.image.load('graphics/husk/husk_2.png').convert_alpha(),(70,70))
            self.frames = [husk,husk_2]
            y_pos = 300
            self.x_speed = 5
            self.type = type

        elif type == 'boss':
            boss = pygame.transform.scale(pygame.image.load('graphics/Boss1/BrokenVessel1.PNG').convert_alpha(),(70,70))
            boss_2 = pygame.transform.scale(pygame.image.load('graphics/Boss1/BrokenVessel2.PNG').convert_alpha(),(70,70))
            self.frames = [boss,boss_2]
            y_pos = 300
            self.x_speed = 2
            self.type = type
            self.direction = -1

        else:
            # fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            # fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            # pygame.transform.scale('location of image' , (60,60))
            
            gruzzer_1 = pygame.transform.scale(pygame.image.load('graphics/gruzzer/gruzzer.png').convert_alpha(), (60,60))
            gruzzer_2 = pygame.transform.scale(pygame.image.load('graphics/gruzzer/gruzzer_2.png').convert_alpha(), (60,60))
            self.frames = [gruzzer_1,gruzzer_2]
            y_pos = 210
            self.x_speed = 4
            self.type = 'gruzzer'

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        
        if self.type == 'boss' :
            self.rect = self.image.get_rect(midbottom = (randint(500,600), y_pos)) # Obstacle Positing x,y RECT
        else:
            self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos)) # Obstacle Positing x,y RECT

        # Init Outcome
        # fly - self.frames , self.image, self.rect, self.animation_index, self.x_speed
    def animation_state(self):
        self.animation_index += 0.1 # Animation
        if self.animation_index >= len(self.frames): self.animation_index = 0 # Animation
        self.image = self.frames[int(self.animation_index)]

    def update(self, game_speed):
        self.animation_state()
        #print("type : " + self.type)
        
        if self.type == 'boss' :
           # |0|--change-|450|--<----|550|-->-|750|--change--|800|

            if self.rect.x < 450 and self.direction < 0: #|->|
                self.direction = self.direction * -1
                print("Boss Speed :",self.x_speed," Boss Location :",self.rect.x)
            elif self.rect.x > 650 and self.direction > 0:
                self.direction = self.direction * -1
                print("Boss Speed :",self.x_speed," Boss Location :",self.rect.x)
            else :
                self.rect.x += round(self.x_speed/game_speed) * self.direction 
        else :    
            self.rect.x -= round(self.x_speed/game_speed)  
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -10: # if obstacle out of canvas range kill sprite (remove from obstacles group)
            self.kill()

