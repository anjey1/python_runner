import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.image = pygame.image.load(
            'graphics/boss/soldier_2.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # player movment
        self.speed = 5
        self.direction = pygame.math.Vector2(0, 0)

        self.gravity = 0.8
        self.jump_speed = -16

    def import_character_assets(self):
        character_path = './graphics/character'
        self.animations = {'idle:[],run:[],jump:[],fall:[],boss:[]'}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations['run']
        # loop over frame index - reset 0 on last image
        self.frame_index += self.animation_speed
        if (self.frame_index >= len(animation)):
            self.frame_index = 0

        # frame_index is double type should convert to int
        self.image = animation[int(self.frame_index)]

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        print(self.direction)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def update(self):
        self.get_input()
        self.animate()
