import pygame
from sys import exit

pygame.init()

#Surface Setup
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner 5')

sky_surf = pygame.image.load('graphics/Sky.png').convert() # 800,300
ground_surf = pygame.image.load('graphics/ground.png').convert() # 800,100

game_active = True # Initial Game State

clock = pygame.time.Clock()
start_time = 0
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # Font File, Font Size
#WoodShop + Initial Location

def display_score():
    current_time = pygame.time.get_ticks() - start_time # get_ticks() - get_ticks()
    # text(string), antialias(true ,false - for pixelart), color #
    score_surf = test_font.render(f'{current_time}', False, (70,70,70,255))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf,score_rect)
    return current_time

#Enemies
#snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()


snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_walk_index = 0
snail_surf = snail_frames[snail_walk_index]

snail_rect = snail_surf.get_rect(bottomright = (600,300))
snail_gravity = 0

#bg
tree_bg = pygame.transform.scale(pygame.image.load('graphics/tree1.png').convert_alpha(), (160,160))
tree_rect = tree_bg.get_rect(bottomright = (0,310))


#player
player_surf = pygame.image.load('graphics\Player\player_stand.png').convert_alpha()
player_rect = player_surf.get_rect(bottomright = (600,300))
player_rect1 = player_surf.get_rect(bottomright = (200,100))
player_rect2 = player_surf.get_rect(bottomright = (300,300)) # 0,0 -> X,Y
player_rect3 = player_surf.get_rect(bottomright = (400,400))


#Engine
while True: # runs 60 times a second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            print('game play')
            if event.type == pygame.KEYDOWN:
                print('Key Down')
                #if event.key == pygame.K_SPACE:
                if event.key == pygame.K_SPACE and snail_rect.bottom >= 300:
                    snail_gravity = -25 # JUMP
                    print('Space')

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_active = True
            print('game restart')
            start_time = pygame.time.get_ticks()

    
    #Logic

    if game_active:
        screen.blit(sky_surf,(0,0))
        screen.blit(tree_bg,tree_rect)
        screen.blit(ground_surf,(0,300)) # this is example of how we set surface on surface - ground_surf on screen    
        score = display_score()
        #Snail
       # snail_rect.x -= 4 # snail_rect.right -= 4
        #if snail_rect.right <= 0: snail_rect.left = 800
        
        player_rect2.x +=6
        if player_rect2.right >= 800: player_rect2.left = 0

        snail_gravity += 1
        snail_rect.y += snail_gravity
        if snail_rect.bottom >= 300: snail_rect.bottom = 300
        screen.blit(snail_surf, snail_rect)

        #bg
        tree_rect.x += 1
        if tree_rect.right >= 800: tree_rect.left = 0
        


        #Player
        player_rect1.x -=2
        player_rect3.y -=1

        screen.blit(player_surf,(0,0))
       # screen.blit(player_surf,player_rect) # Image (File), (600,300)
        screen.blit(player_surf,player_rect1)
        screen.blit(player_surf,player_rect2)
        screen.blit(player_surf,player_rect3)
        
        # Snail Animation
        snail_walk_index += 0.1
        print(snail_walk_index)
        if snail_walk_index >= len(snail_frames): snail_walk_index = 0 # reset snail walk index
        print(snail_walk_index)
        snail_surf = snail_frames[int(snail_walk_index)]

        if player_rect2.colliderect(snail_rect):
            print('collision')
            game_active = False
            snail_rect.x = 600
            player_rect2.x = 80







    else:
        screen.fill((200,150,20)) # (R,G,B)
        test_font = pygame.font.Font('font/Pixeltype.ttf', 50) # Font File, Font Size
        test_surf = test_font.render(f'Game Over - Your Score {score}', False, (70, 70, 70, 255)) # Text , Pixelize, Color R G B, Brightness 
        test_surf2 = test_font.render('Press - R To Restart', False, (70, 70, 70, 255)) # Text , Pixelize, Color R G B, Brightness 
        test_rect = test_surf.get_rect(center = (350,50)) # X, Y
        test_rect2 = test_surf2.get_rect(center = (400,250)) # X, Y
        screen.blit(test_surf,test_rect)
        screen.blit(test_surf2,test_rect2)

    
    pygame.display.update()
    clock.tick(60) # this loop will run 60 time a second