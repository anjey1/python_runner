import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos) -> None:
        super().__init__()
        # self.import_character_assets()
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

    def clip(surface, x, y, x_size, y_size):  # Get a part of the image
        handle_surface = surface.copy()  # Sprite that will get process later
        clipRect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
        handle_surface.set_clip(clipRect)  # Clip or you can call cropped
        image = surface.subsurface(handle_surface.get_clip())  # Get subsurface
        return image.copy()  # Return

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
