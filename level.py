import pygame
from settings import *
from game_data import levels
from tile import Tile

#self.image = pygame.Surface((100, 70))


class Level:
    def __init__(self, current_level, surface, create_overworld) -> None:

        # level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.create_overworld = create_overworld

        # level display
        self.font = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.text_surf = self.font.render(
            level_content, True, (170, 210, 70, 255))
        self.text_rect = self.text_surf.get_rect(
            center=(screen_width / 2, screen_height / 2))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)


class Level_Single:
    def __init__(self, level_data, surface) -> None:
        self.display_surface = surface
        self.setup_level(level_data)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.draw(self.display_surface)
