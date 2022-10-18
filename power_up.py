
import pygame

from random import randint

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type = 'seed', powerup_init_y = 300 ):
        super().__init__()

        if type == 'seed':
            seed_image = pygame.image.load('graphics/light_seed/light_seed.png').convert_alpha()
            seed_image_2 = pygame.image.load('graphics/light_seed/light_seed_2.png').convert_alpha()
            self.frames = [seed_image,seed_image_2] # Array
            y_pos = powerup_init_y
            self.x_speed = 4
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos)) # PowerUp Positing x,y RECT
        
        # X :  0 -------- 800 | 900-1100 - we draw the sprites outside screen

    def update(self):
        self.animation_state()
        
        self.rect.x -= self.x_speed # fly - 5 | snail - 6 | pika - 8 
        
        
    def animation_state(self):
        self.animation_index += 0.1 # Animation
        if self.animation_index >= len(self.frames): self.animation_index = 0 # Animation
        self.image = self.frames[int(self.animation_index)]
