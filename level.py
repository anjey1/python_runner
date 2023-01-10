import pygame
from settings import *
from game_data import levels
from tile import Tile
from player import Player

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

        # Level Setup

        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles_group.add(tile)
                if cell == 'P':
                    player = Player((x, y))
                    self.player_group.add(player)

    def scroll_x(self):
        player = self.player_group.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 5
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -5
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 5

    def horizontal_movment_collision(self):
        player = self.player_group.sprite
        player.rect.x += player.direction.x * player.speed

        # Collision Engine
        for sprite in self.tiles_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # Moving Left
                    player.rect.left = sprite.rect.right
                elif player.direction.x > 0:  # Moving Right
                    player.rect.right = sprite.rect.left

    def vertical_movment_collision(self):
        player = self.player_group.sprite
        player.apply_gravity()

        # Collision Engine
        for sprite in self.tiles_group.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:  # Moving Down when gravity is Vector(0,0.8) |0 -> 400|
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # Cancel Gravity
                elif player.direction.y < 0:  # Moving Up
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0  # Cancel Gravity

    def run(self):

        # Level Tiles
        self.tiles_group.update(self.world_shift)
        self.tiles_group.draw(self.display_surface)
        self.scroll_x()

        # Level Player
        self.player_group.update()
        self.horizontal_movment_collision()
        self.vertical_movment_collision()
        self.player_group.draw(self.display_surface)
