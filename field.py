from camera import *
from mouse import *
import pygame


# need to draw static map
# all changes should be tracked
# do not redraw static map on the same level

class Field():
    def __init__(self, surface, blocks, block_size, player):
        self.screen = surface
        self.camera = Camera((surface.get_width(), surface.get_height()), (block_size, block_size))
        self.mouse = Mouse()
        self.player = player
        self.enemies = []
        self.blocks = blocks
        self.block_size = block_size
        self.dyn_obj = {'player': [self.player], 'enemies': self.enemies}
        self.map = []
        self.tiles = [] 
        self.static_map = None
        self.dynamic_map = None

    def update(self):
        
        self.fill_dynamic_map()
        
        for enemy in self.enemies:
            enemy.move(self.tiles)
            enemy.update()
        
        self.player.move(self.tiles)
        self.player.update()

        self.mouse.update(self.camera.rect.topleft)
        self.camera.update(self.player.rect)
        
        # for testing mouse position
        self.mouse.collides(self.tiles)
        for elem in self.mouse.collisions:
            pygame.draw.rect(self.dynamic_map, (200, 200, 0), elem)
        
        
        self.screen.blit(self.dynamic_map, (0, 0),  self.camera.rect)

        pygame.display.flip()    
        
        self.screen.fill((200, 200, 200))


    def fill_dynamic_map(self):
        self.dynamic_map = self.static_map.copy()
        for name, container in self.dyn_obj.items():
            for obj in container:
                self.dynamic_map.blit(obj.surf, obj.rect)
            
    
    def set_static_map(self):
        self.static_map = pygame.Surface((self.block_size * len(self.map[0]), self.block_size * len(self.map)))
        self.static_map.fill((200, 200, 200))
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                x_coord, y_coord = j * self.block_size, i * self.block_size
                cur_block = self.blocks.get(self.map[i][j])
                if cur_block is not None: # check if block is static
                    self.static_map.blit(cur_block, (x_coord, y_coord))
                    self.tiles.append(pygame.Rect(x_coord, y_coord, self.block_size, self.block_size))    
    
    def load_map(self, map_path):
        with open(map_path) as f:
            self.map = [list(string) for string in f.read().split('\n')]
        self.set_static_map()
