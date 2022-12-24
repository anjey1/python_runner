import pygame

def display_score(screen, start_time, test_font):
    current_time = pygame.time.get_ticks() - start_time
    # text(string), antialias(true ,false - for pixelart), color #
    score_surf = test_font.render(f'{current_time}', False, (70,70,70,255))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf,score_rect)
    return current_time

# Example (lives = 3) default value if not passed to function
def display_lives(screen, lives):
    for i in range(lives):
        player_life = pygame.transform.scale(pygame.image.load('graphics/Player/jump.png').convert_alpha(), (30,30))
        player_life_rect = player_life.get_rect(center = (50 + i * 30, 50))
        screen.blit(player_life,player_life_rect)

def collision_sprites(player, obstacle_group, weapons_boss):
    
    if pygame.sprite.spritecollide(player.sprite, weapons_boss, False, collided = None):
        print('Weapon Group Player Collision')
        return False

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, collided = None): # sprite, group, dokill = kill group sprite on colission, collided = None
        obstacle_group.empty()
        return False
    else: 
        return True



def collision_powerup(player, powerup_group):
    if pygame.sprite.spritecollide(player.sprite, powerup_group, True, collided = None): # google pygame groupcollide
        return True
    return False