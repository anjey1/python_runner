
import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, type = 'axe', weapon_init_y = 300 ):
        super().__init__()

        self.weapon_group = []
        self.obstacle_group = []

        if type == 'fireball':
            self.image = pygame.transform.scale(pygame.image.load('graphics/fireball.png').convert_alpha(), (60,60))
            self.rect = self.image.get_rect(midbottom = (80,weapon_init_y))
        else:
            self.image = pygame.transform.scale(pygame.image.load('graphics/axe.png').convert_alpha(), (60,60))
            self.rect = self.image.get_rect(midbottom = (80,weapon_init_y))

        #self.throw_sound = pygame.mixer.Sound("audio/matches.wav")
        #self.throw_sound.set_volume(0.1)  

    def weapon_input(self):
        keys = pygame.key.get_pressed()
        # if game_active and keys[pygame.K_f] :
        #     pygame.mixer.Sound.play(self.throw_sound)

        # Dictionary
        # {
        #    "name" : "Avi",
        #    "age" : 15
        #    "city" : Haifa 
        # }
        #
        #

    def update(self, weapons_group, obstacle_group ):
        self.weapons_group = weapons_group
        self.obstacle_group = obstacle_group
        self.weapon_input()
        self.rect.x += 5
        self.destroy()

    def destroy(self):
        if pygame.sprite.groupcollide(self.weapons_group, self.obstacle_group, True, True): # google pygame groupcollide
            print('Group Colided !!!!')
            self.kill()
