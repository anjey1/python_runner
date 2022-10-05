import pygame
from game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status,icon_speed) -> None:
        super().__init__()
        self.image = pygame.Surface((100, 70))
        if status == 'open':
            self.image.fill((255,0,0))
            self.image = pygame.image.load('Assets/cloud.png').convert_alpha();
        else:
            self.image.fill((128,128,128))
            self.image = pygame.image.load('Assets/cloud.png').convert_alpha();                        
        self.rect = self.image.get_rect(center = pos)

        # Rect(left, top, width, height)
        self.detection_zone = pygame.Rect(
            self.rect.centerx - (icon_speed/3),
            self.rect.centery - (icon_speed/3),
            icon_speed*3,
            icon_speed*3)
        
    def get_detect_zone(self):
        return self.detection_zone  

class Icon(pygame.sprite.Sprite):
    def __init__(self,pos) -> None:
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20,20))
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect(center = pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level) -> None:       
        # Setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movment logic
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.moving = False

        # sprites
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        # Group of sprites
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'],'open', self.speed)
            else:
                node_sprite = Node(node_data['node_pos'],'lock', self.speed)
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        # sprites() - list of the Sprites this Group contains
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)
    

    def update_box_pos(self):
        for index, node in enumerate(self.nodes.sprites()):
            if index > -1:
                pygame.draw.rect(self.display_surface, (255,255,255), 
                pygame.Rect(
                node.detection_zone.x,
                node.detection_zone.y,
                node.detection_zone.width,
                node.detection_zone.height
                )
            ,10)
            print('new_box', node.detection_zone)
                   

    def update_icon_pos(self):
        #self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        if self.move_direction and self.moving:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
      
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                self.icon.sprite.pos = (target_node.rect.centerx,target_node.rect.centery)
                
     

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movment_data('next') # <Vector2(0.73994, -0.672673)>
                #print(self.move_direction)
                self.current_level +=1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movment_data('pervious') # <Vector2(0.73994, -0.672673)>
                self.current_level -=1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)
            
    def get_movment_data(self,target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else: 
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)
        return (end -start).normalize()
 
    def draw_paths(self):
        # pointlist = [ node['node_pos'] for node in levels.values() ]
        pointlist = [ node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level ]
        pygame.draw.lines(self.display_surface, (255,0,0), False, pointlist, 6)                                
    
    def run(self):
        self.input()
        self.update_icon_pos()
        self.icon.update()
        
        self.draw_paths()
       
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        # self.update_box_pos()
        