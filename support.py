from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for path_src, folder, images_array in walk(path):
        for image in images_array:
            full_path = path + '/' + image
            print(full_path)
            image_surf = pygame.image.load(
                './graphics/character/boss/soldier_2.png')
            # self.image = pygame.image.load('Assets/cloud.png').convert_alpha();
            surface_list.append(image_surf)

    return surface_list


def clip(surface, x, y, x_size, y_size):  # Get a part of the image
    handle_surface = surface.copy()  # Sprite that will get process later
    clipRect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
    handle_surface.set_clip(clipRect)  # Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip())  # Get subsurface
    return image.copy()  # Return


import_folder('./graphics/character/boss')
