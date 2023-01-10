from os import walk
import pygame


def import_folder(path):
    surface_list = []


    for path_src, folder, images_array in walk(path):
        for image in images_array:
            full_path = path + '/' + image
            print(full_path)
            image_surf = pygame.image.load('./graphics/character/boss/soldier_2.png')
            # self.image = pygame.image.load('Assets/cloud.png').convert_alpha();
            surface_list.append(image_surf)
    
    return surface_list


import_folder('./graphics/character/boss')
