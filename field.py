from camera import *
from mouse import *
from lifeless_objects import *
from live_objects import *
from constants import Constant
import pygame

class Field():
    def __init__(self, surface, player):
        self.screen = surface
        self.camera = Camera((surface.get_width(), surface.get_height()), (4 * Constant.TILE_SIZE, 2 * Constant.TILE_SIZE))
        self.mouse = Mouse()
        self.player = player
        self.enemies = []
        self.blocks = None
        self.dyn_obj = {'player': [self.player], 'enemies': self.enemies, 'blocks' : []}
        self.map = []
        self.tiles = [] 
        self.static_map = None
        self.dynamic_map = None
        self.add_blocks()
        self.add_enemies()
        self.init_mixer()
        self.load_map('maps/02.txt')

    def add_enemies(self):
        fname = 'sprites/live_objects/'
        self.enemies.append(MovingGuy(fname + 'Golem_Idle_1.png', (Constant.TILE_SIZE*2, Constant.TILE_SIZE*2), target = self.player))
        self.enemies[-1].surf.set_colorkey('white')

        self.enemies.append(Enemy(fname + 'LargeMushroom_Idle_1.png', size =(Constant.TILE_SIZE*3, Constant.TILE_SIZE*3)))
        self.enemies.append(Enemy(fname + 'LargeMushroom_Idle_1.png'))
        self.enemies.append(Enemy(fname + 'LargeMushroom_Idle_1.png'))
        self.enemies.append(Enemy(fname + 'LargeMushroom_Idle_1.png'))
        
        self.enemies.append(MovingGuy(fname + 'Fairy_Idle_1.png', target = self.player))
        self.enemies.append(MovingGuy(fname + 'Fairy_Idle_1.png', target = self.player))
        self.enemies.append(MovingGuy(fname + 'Fairy_Idle_1.png', target = self.player))

        
        for i, enemy in enumerate(self.enemies):
            enemy.rect = enemy.rect.move(self.camera.get_xoffset() + (i + 1)*Constant.TILE_SIZE, self.camera.get_yoffset() + (i + 1)*Constant.TILE_SIZE*2)

    
    def add_blocks(self):
        fname = 'sprites/ground/ground_'
        self.blocks = {
            'w' : StaticBlock(image = fname + 'grass.png'),
            'q' : StaticBlock(image = fname + 'up_left.png'),
            'e' : StaticBlock(image = fname + 'up_right.png'),
            'a' : StaticBlock(image = fname + 'left.png'),
            's' : StaticBlock(image = fname + 'midle.png'),
            'd' : StaticBlock(image = fname + 'right.png'),
            'z' : StaticBlock(image = fname + 'low_left.png'),
            'x' : StaticBlock(image = fname + 'low.png'),
            'c' : StaticBlock(image = fname + 'low_right.png'),
            'm' : DynamicBlock(image = fname + 'move.png')
        }
    
    def init_mixer(self):
        pygame.mixer.music.load('sound/magic-cliffs.wav')
        pygame.mixer.music.play(-1)
    
    def update(self):
        self.fill_dynamic()
        
        self.player.move(*self.tiles, *self.enemies)
        self.player.update()
        
        for enemy in self.enemies:
            enemy.move(self.player, *self.tiles)
            enemy.update()
        
        for block in self.dyn_obj['blocks']:
            block.move()
        
        self.mouse.update(self.camera.rect.topleft)
        self.camera.update(self.player)
        
        # for testing mouse position
        self.mouse.collides(*self.tiles)
        
        for elem in self.mouse.collisions:
            pygame.draw.rect(self.dynamic_map, 'bisque', elem)
        
        self.screen.blit(self.dynamic_map, (0, 0),  self.camera.rect)

        pygame.display.flip()
        
        self.screen.fill('grey')
        
    def fill_dynamic(self):
        self.dynamic_map = self.static_map.copy()
        for name, container in self.dyn_obj.items():
            for obj in container:
                self.dynamic_map.blit(obj.surf, obj.rect)
            
    
    def fill_static(self):
        self.static_map = pygame.Surface((Constant.TILE_SIZE * len(self.map[0]), Constant.TILE_SIZE * len(self.map)))
        background_image = pygame.image.load('sprites/background/mountains.png')
        background_image = pygame.transform.scale(background_image, [3840, 2000])
        self.static_map.blit(background_image, (0, 0))
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                x_coord, y_coord = j * Constant.TILE_SIZE, i * Constant.TILE_SIZE
                cur_block = self.blocks.get(self.map[i][j])
                if isinstance(cur_block, Block):
                    cur_block = cur_block.get_moved_block(x_coord, y_coord)
                    if isinstance(cur_block, StaticBlock): # check if block is static
                        self.static_map.blit(cur_block.surf, (x_coord, y_coord))
                        self.tiles.append(cur_block)
                    elif isinstance(cur_block, DynamicBlock):
                        self.dyn_obj['blocks'].append(cur_block)
                        self.tiles.append(cur_block)
            
    
    def load_map(self, map_path):
        self.static_map = None
        self.dynamic_map = None
        self.tiles = list()
        self.dyn_obj['blocks'] = list()
        with open(map_path) as f:
            self.map = [list(string) for string in f.read().split('\n')]
        self.fill_static()