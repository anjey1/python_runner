import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # X, Y - (size,size)
        self.image = pygame.Surface((size, size))
        self.image.fill((200, 150, 20))
        self.rect = self.image.get_rect(topleft=pos)
