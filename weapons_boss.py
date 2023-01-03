
import pygame


class Weapon_Boss(pygame.sprite.Sprite):
    def __init__(self, type = 'axe', boss = pygame.sprite.Sprite):
        super().__init__()

        self.weapon_group = []
        self.obstacle_group = []
        boss_x = boss.x
        boss_y = boss.y + 50
       
        
        if type == 'fireball':
            self.image = pygame.transform.scale(pygame.image.load('graphics/fireball.png').convert_alpha(), (60,60))
            self.rect = self.image.get_rect(midbottom = (boss_x, boss_y))
        else:
            self.image = pygame.transform.scale(pygame.image.load('graphics/axe.png').convert_alpha(), (60,60))
            self.rect = self.image.get_rect(midbottom = (boss_x, boss_y))

        #self.throw_sound = pygame.mixer.Sound("audio/matches.wav")
        #self.throw_sound.set_volume(0.1)  

    def weapon_input(self):
        keys = pygame.key.get_pressed()
        # if game_active and keys[pygame.K_f] :
        #     pygame.mixer.Sound.play(self.throw_sound)


    def update(self, weapons_group, player ):
        self.weapons_group = weapons_group
        # self.obstacle_group = obstacle_group
        # self.weapon_input()
        self.rect.x -= 5
        self.destroy(player)

    def destroy(self, player):
        if pygame.sprite.groupcollide(self.weapons_group, player, False, False): # google pygame groupcollide
            print('Boss Weapon Group Colided !!!!')
            # self.kill()
