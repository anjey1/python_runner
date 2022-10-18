import pygame

pygame.init()

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner Gamer')

test_surface = pygame.Surface((100,200))
test_surface.fill((50,100,20,255))
test_rect = test_surface.get_rect(center = (100,200))

clock = pygame.time.Clock()

#Engine
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    test_rect.x += 4
    screen.blit(test_surface,(100,200))
    
    pygame.display.update()
    clock.tick(60)