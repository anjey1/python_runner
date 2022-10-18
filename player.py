import pygame

class Player(pygame.sprite.Sprite): # self -> Player
    def __init__(self,game_active_orig):
        super().__init__()

        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2] # 0,1
        self.player_animation_index = 0

        self.image = self.player_walk[int(self.player_animation_index)]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.jump_sound.set_volume(0.2)        
        self.game_active = game_active_orig

    def player_input(self,player_gravity):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and self.game_active: # if space & not in air
            self.gravity = -player_gravity # move player up to 280
            pygame.mixer.Sound.play(self.jump_sound)
    
    def apply_gravity(self):
        self.gravity += 1 # move player down
        self.rect.y += self.gravity
        # print(game_active)
        if self.rect.bottom >= 300: # if not in air place on 300
            self.rect.bottom = 300
    
    def amnimation_state(self):
        if self.rect.bottom < 300: # if player in air [280 when jumping < 300]
            self.image = self.player_jump # self.image = jump image
        else:
            self.player_animation_index += 0.1 # Animation using int for 0 - 0.9 -> 0 || 1 - 1.9 -> 1 [0,1]

            # len gets the length of array which is 2 [0,1]
            # 0.5 > 2 ? False | 2.1 > 2 ? True  - Set index to 0
            if self.player_animation_index >= len(self.player_walk): self.player_animation_index = 0 # Animation
            self.image = self.player_walk[int(self.player_animation_index)] # int for 0 - 0.9 -> 0 || 1 - 1.9 -> 1 [0,1]

    def update(self,player_gravity,game_active_current):
        self.player_input(player_gravity)
        self.apply_gravity()
        self.amnimation_state()
        self.destroy()
        self.game_active = game_active_current
    
    def destroy(self):
        if not self.game_active: # if game ended on jump place back to ground
            self.rect.bottom = 300