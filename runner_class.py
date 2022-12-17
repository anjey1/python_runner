
import pygame
# C:\Users\marius\AppData\Local\Programs\Python\Python37\Lib\site-packages
from random import choice
from sys import exit

#Classes
from player import Player
from obstacle import Obstacle   
from weapons import Weapon
from power_up import PowerUp

# Functions

# from functions.py import function, function, function
from functions import display_score, display_lives, collision_sprites, collision_powerup        

pygame.init()

#bg_music = pygame.mixer.Sound('audio/music.wav')
#bg_music.set_volume(0.1)
#bg_music.play(loops = -1) # Infinite loops

# State
start_time = 0
score = 0
game_speed = 1
player_gravity = 20
mode = False
powerup_taken_last = 0
powerup_cooldown = 3000
fired_last = 0
weapon_cooldown = 1500
lives = 5
levelCycle = 5000
boss_mode = False

#Surface Setup
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True

#Player
player = pygame.sprite.GroupSingle()
player.add(Player(game_active))

#Enemies
obstacle_group = pygame.sprite.Group()

#Power Up
powerup_group = pygame.sprite.Group()

#Background
background_group = pygame.sprite.Group()

#Weapons
weapons_group = pygame.sprite.Group()

#Boss Weapons
weapons_boss_group = pygame.sprite.Group()

#Timers
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer, 1500) #Rewspawn Speed

powerup_timer = pygame.USEREVENT +2
pygame.time.set_timer(powerup_timer, 10000) # Animation Speed

boss_fire = pygame.USEREVENT +3
pygame.time.set_timer(boss_fire, 3000) # Animation Speed
# 800 pixel - 60*4 - 240 pixel per second - 3.3 second

# fly_animation_timer = pygame.USEREVENT +3
# pygame.time.set_timer(fly_animation_timer,100) # Animation Speed

# back_animation_timer = pygame.USEREVENT +4
# pygame.time.set_timer(back_animation_timer, 2500) # Animation Speed


#Engine - Here Logic Starts
while True:
    #Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #mouseEvents()
            if event.type == pygame.KEYUP:
                print('Key Up')            
            if event.type == pygame.KEYDOWN:
                print('Key Down')
                if event.key == pygame.K_f:
                    print('Fire')
                    
                    if pygame.time.get_ticks() - fired_last > weapon_cooldown:  # weapons cooldown
                        weapons_group.add(Weapon('axe',player.sprite.rect.y + 70))
                        fired_last = pygame.time.get_ticks() # time stamp for power up start time

            if event.type == obstacle_timer: # Draw/Spawn Enemies
                obstacle_group.add(Obstacle(choice(['fly','fly','husk'])))

            if event.type == powerup_timer:
                print('PowerUp Added')
                powerup_group.add(PowerUp(choice(['seed','seed','seed'])))

            # if event.type == back_animation_timer: # Draw/Spawn Background
            #     background_group.add(Background(choice(['tree','waterfall','tree'])))                
            
            
            if levelCycle - pygame.time.get_ticks() < 0 & boss_mode == False :  # level end

                if not boss_mode :
                    obstacle_group.empty()
                    powerup_group.empty() 
                    pygame.time.set_timer(obstacle_timer, 0)        
                    pygame.time.set_timer(powerup_timer, 0)
                    print('Boss MODE');
                    obstacle_group.add(Obstacle('boss')) 
                                

                boss_mode = True
                #Boss True
                if event.type == boss_fire: # Draw/Spawn Enemies
                    weapons_boss_group.add(Weapon('fireball',obstacle_group.sprites()[0].rect.y + 100))
                    print('boss_fired')

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                start_time = pygame.time.get_ticks()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                pygame.quit()
                exit()
            
    #Logic Loop - runs 60 times a sec
    if game_active: # if True show Game if False Show Screen - Restart Exit
        
        #Background

        screen.blit(sky_surf,(0,0)) # Draw sky on sky surface (Image, Where to put it)- pygame.blit google it
        background_group.draw(screen)
        background_group.update()
        screen.blit(ground_surf,(0,300)) # this is example of how we set surface on surface        

        score = display_score(screen, start_time, test_font)
        display_lives(screen, lives)

        #Obstacle
        
        obstacle_group.draw(screen)
        obstacle_group.update(game_speed)
        
        #Player

        player.draw(screen)
        player.update(player_gravity,game_active)

        # Weapons
        weapons_group.draw(screen)
        weapons_group.update(weapons_group, obstacle_group)

        weapons_boss_group.draw(screen)
        weapons_boss_group.update(weapons_boss_group, player)
        
        

        # Powerup
        powerup_group.draw(screen)
        powerup_group.update()
        

        #Collision
        if not collision_sprites(player, obstacle_group):
             print('Colided')
             lives -= 1
             if(lives < 1):
                 game_active = False
        

        #game_active = collision_sprites() # when collision happens return FALSE
        
        if collision_powerup(player, powerup_group): # Function return True/False
            game_speed = 2
            powerup_taken_last = pygame.time.get_ticks() # time stamp for power up start time

            powerUp_sound = pygame.mixer.Sound("audio/powerUp.wav")
            powerUp_sound.set_volume(0.2)
            pygame.mixer.Sound.play(powerUp_sound)

            player_gravity = 23
        
        if game_speed > 1:
            # 100000000 - 999996595 > 3000 | now - power_up_taken_time > power_up_cooldown
            if pygame.time.get_ticks() - powerup_taken_last > powerup_cooldown: 
                game_speed = 1
                player_gravity = 20
        
    else:
        
        #Reset On Game Over
        screen.fill((200,150,20))
        
        score_end_surf = test_font.render(f'Your Score - {score}', False, (70,70,70,255))
        end_surf = test_font.render('Game Over', True, (70,70,70,255))
        end_surf2 = test_font.render('Press R - To Restart | Press E - To Exit', True, (70,70,70,255))
        player_zoom = pygame.transform.rotozoom(pygame.image.load('graphics/Player/jump.png').convert_alpha(), 0, 2)

        end_rect = end_surf.get_rect(center = (400, 50))
        end_rect2 = end_surf.get_rect(center = (225, 350))
        score_end_rect = score_end_surf.get_rect(center = (375,80))
        player_zoom_rect = player_zoom.get_rect(center = (370, 200))
        player.update(player_gravity, game_active) # update player on game over

        screen.blit(end_surf,end_rect)
        screen.blit(end_surf2,end_rect2)
        screen.blit(player_zoom,player_zoom_rect)
        screen.blit(score_end_surf,score_end_rect)

    pygame.display.update()
    clock.tick(60) # this loop will run 60 time a second

    # R 0-255 G 0-255 B 0-255 - (tuple) \ #rrggbb - 00-ff  00-ff  00-ff - 64 64 64 #c0e8ec
    #pygame.draw.line(screen, (250,15,200,255), (score_rect.x,score_rect.y), (player_rect.x,player_rect.y),5)
    #pygame.draw.line(screen, (250,15,200,255), (300,300), pygame.mouse.get_pos(),5)
    #pygame.draw.ellipse(screen, (200,115,70,255), pygame.Rect(50,200,100,100))
    