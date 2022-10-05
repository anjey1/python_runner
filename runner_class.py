from pickle import TRUE
from random import randint, choice
from overworld import Overworld
from level import Level
import pygame
from sys import exit

# Classes


class Game:
    def __init__(self):
        self.max_level = 5
        # Game Class -> Method to create the overworld -> level
        # Game Class -> Methos to create level -> overworld
        self.overworld = Overworld(
            1, self.max_level, screen, self.create_level)
        self.status = 'overworld'
        #self.level = Level(3,screen)

    def create_level(self, current_level):
        print('Current level:', current_level)
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, current_level, new_max_level):
        print('Current Overworld:', current_level)
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load(
            'graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/Player/player_walk_2.png').convert_alpha()
        self.player_jump = pygame.image.load(
            'graphics/Player/jump.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_animation_index = 0

        self.image = self.player_walk[int(self.player_animation_index)]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.wav")
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if game_active and keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            pygame.mixer.Sound.play(self.jump_sound)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def amnimation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_animation_index += 0.1  # Animation
            if self.player_animation_index >= len(self.player_walk):
                self.player_animation_index = 0  # Animation
            self.image = self.player_walk[int(self.player_animation_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.amnimation_state()
        self.destroy()

    def destroy(self):
        if not game_active:
            self.rect.bottom = 300


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'snail':
            snail_1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 210
        else:
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1  # Animation
        if self.animation_index >= len(self.frames):
            self.animation_index = 0  # Animation
        self.image = self.frames[int(self.animation_index)]

    def update(self, game_speed):
        self.animation_state()
        self.rect.x -= round(6/game_speed)
        self.destroy()

    def destroy(self):
        if self.rect.x <= -10:
            self.kill()


class Background(pygame.sprite.Sprite):
    def __init__(self, type='tree'):
        super().__init__()

        if type == 'tree':
            self.image = pygame.transform.scale(pygame.image.load(
                'graphics/tree1.png').convert_alpha(), (160, 160))
            self.rect = self.image.get_rect(midbottom=(800, 320))
        else:
            self.image = pygame.transform.scale(pygame.image.load(
                'graphics/LPC Base Assets/tiles/waterfall.png').convert_alpha(), (160, 160))
            self.rect = self.image.get_rect(midbottom=(800, 330))

    def update(self):
        self.rect.x -= 2

    def destroy(self):
        if self.rect.x <= 0:
            self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, type='axe', weapon_init_y=300):
        super().__init__()

        if type == 'fireball':
            self.image = pygame.transform.scale(pygame.image.load(
                'graphics/fireball.png').convert_alpha(), (60, 60))
            self.rect = self.image.get_rect(midbottom=(80, weapon_init_y))
        else:
            self.image = pygame.transform.scale(pygame.image.load(
                'graphics/axe.png').convert_alpha(), (60, 60))
            self.rect = self.image.get_rect(midbottom=(80, weapon_init_y))

        self.throw_sound = pygame.mixer.Sound("audio/matches.wav")
        self.throw_sound.set_volume(0.1)

    def weapon_input(self):
        keys = pygame.key.get_pressed()
        if game_active and keys[pygame.K_f]:
            pygame.mixer.Sound.play(self.throw_sound)

    def update(self):
        self.weapon_input()
        self.rect.x += 5
        self.destroy()

    def destroy(self):
        if pygame.sprite.groupcollide(weapons_group, obstacle_group, True, True):
            print('Group Colided !!!!')
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'onion':
            self.frames = [
                pygame.image.load('Assets/onion.png').convert_alpha(),
                pygame.image.load('Assets/onion_jump.png').convert_alpha()
            ]
            y_pos = 210
        else:
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1  # Animation
        if self.animation_index >= len(self.frames):
            self.animation_index = 0  # Animation
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 3
        self.destroy()

    def destroy(self):
        if self.rect.x <= -10:
            self.kill()

# Functions


def display_score():
    current_time = pygame.time.get_ticks() - start_time
    # text(string), antialias(true ,false - for pixelart), color #
    score_surf = test_font.render(f'{current_time}', False, (70, 70, 70, 255))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprites():
    # sprite, group, dokill = kill group sprite on colission, collided = None
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, collided=None):
        obstacle_group.empty()
        return False
    else:
        return True


def powerup_collision():
    # sprite, group, dokill = kill group sprite on colission, collided = None
    if pygame.sprite.spritecollide(player.sprite, powerup_group, True):
        powerup_group.empty()
        return TRUE
    else:
        return False
# Setup


pygame.init()

# bg_music = pygame.mixer.Sound('audio/music.wav')
# bg_music.play(loops = -1) # loops = 5 - will play 6 time loops = -1 Infinite Times

# Surface Setup

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')

clock = pygame.time.Clock()
start_time = 0
score = 0
game = Game()
game_speed = 1


# Draw

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
game_started = False
powerup_active = False
powerup_taken_last = 0
powerup_cooldown = 3000

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Enemies
obstacle_group = pygame.sprite.Group()

# Background
background_group = pygame.sprite.Group()

# Weapons
weapons_group = pygame.sprite.Group()

# Powerup
powerup_group = pygame.sprite.Group()

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)  # Rewspawn Speed

powerup_time = pygame.USEREVENT + 2
pygame.time.set_timer(powerup_time, 3000)  # Animation Speed

back_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(back_animation_timer, 2500)  # Animation Speed


# Engine
while True:
    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # mouseEvents()
            if event.type == pygame.KEYUP:
                print('Key Up')
            if event.type == pygame.KEYDOWN:
                print('Key Down')
                if event.key == pygame.K_f:
                    print('Fire')
                    weapons_group.add(Weapon('axe', player.sprite.rect.y + 70))

            if event.type == obstacle_timer:  # Draw/Spawn Enemies
                obstacle_group.add(Obstacle(choice(['fly', 'fly', 'snail'])))
            if event.type == back_animation_timer:  # Draw/Spawn Background
                background_group.add(Background(
                    choice(['tree', 'waterfall', 'tree'])))
            if event.type == powerup_time:
                powerup_group.add(PowerUp(choice(['onion', 'onion'])))

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_active = True
            start_time = pygame.time.get_ticks()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            game_active = True
            game_started = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            pygame.quit()
            exit()

    # Logic Loop
    if game_active:

        # Background

        screen.blit(sky_surf, (0, 0))
        background_group.draw(screen)
        background_group.update()
        # this is example of how we set surface on surface
        screen.blit(ground_surf, (0, 300))

        score = display_score()

        # Obstacle

        obstacle_group.draw(screen)
        obstacle_group.update(game_speed)

        # Player

        player.draw(screen)
        player.update()

        # Weapons
        weapons_group.draw(screen)
        weapons_group.update()

        # Powerup
        powerup_group.draw(screen)
        powerup_group.update()

        # Collision
        game_active = collision_sprites()

        if powerup_collision():
            game_speed = 2
            powerup_taken_last = pygame.time.get_ticks()
            powerup_sound = pygame.mixer.Sound("audio/powerUp.wav")
            powerup_sound.set_volume(0.2)
            pygame.mixer.Sound.play(powerup_sound)
            print('power up taken !')

        if game_speed > 1:
            if pygame.time.get_ticks() - powerup_taken_last > powerup_cooldown:
                game_speed = 1
                print('power up removed !')

    else:
        background_image = pygame.image.load('graphics/opening.png').convert()
        screen.blit(background_image, (0, 0))

        if game_started:
            # Reset On Game Over

            # screen.fill((200,150,20))

            score_end_surf = test_font.render(
                f'Your Score - {score}', False, (70, 70, 70, 255))
            end_surf = test_font.render('Game Over', True, (70, 70, 70, 255))
            end_surf2 = test_font.render(
                'Press R - To Restart | Press E - To Exit', True, (70, 70, 70, 255))
            player_zoom = pygame.transform.rotozoom(pygame.image.load(
                'graphics/Player/jump.png').convert_alpha(), 0, 2)

            end_rect = end_surf.get_rect(center=(400, 50))
            end_rect2 = end_surf.get_rect(center=(225, 350))
            score_end_rect = score_end_surf.get_rect(center=(375, 80))
            player_zoom_rect = player_zoom.get_rect(center=(370, 200))
            player.update()

            screen.blit(end_surf, end_rect)
            screen.blit(end_surf2, end_rect2)
            screen.blit(player_zoom, player_zoom_rect)
            screen.blit(score_end_surf, score_end_rect)

        else:
            # Reset On Game Over
            # screen.fill((255,250,250))

            end_surf = test_font.render(
                'Welcome To Runner', False, (70, 70, 70, 255))
            end_surf2 = test_font.render(
                'Start The Game - Press S', True, (70, 70, 70, 255))
            end_rect = end_surf.get_rect(center=(400, 20))
            end_rect2 = end_surf.get_rect(center=(370, 50))
            screen.blit(end_surf, end_rect)
            screen.blit(end_surf2, end_rect2)
            game.run()

    pygame.display.update()
    clock.tick(60)  # this loop will run 60 time a second

    # R 0-255 G 0-255 B 0-255 - (tuple) \ #rrggbb - 00-ff  00-ff  00-ff - 64 64 64 #c0e8ec
    #pygame.draw.line(screen, (250,15,200,255), (score_rect.x,score_rect.y), (player_rect.x,player_rect.y),5)
    #pygame.draw.line(screen, (250,15,200,255), (300,300), pygame.mouse.get_pos(),5)
    #pygame.draw.ellipse(screen, (200,115,70,255), pygame.Rect(50,200,100,100))
