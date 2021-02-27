from camera import *
import pygame

class Field():
    def __init__(self, surface, init_level, blocks, block_size, player):
        self.map = init_level
        self.screen = surface
        self.camera = Camera(surface.get_size(), (surface.get_width()//10, surface.get_height()//10))
        self.tiles = [] 
        self.player = player
        self.blocks = blocks
        self.block_size = block_size
        
    def update(self):
        self.player.physics.update()

        self.camera.update(self.player.rect)


        self.screen.blit(self.player.surf, self.player.rect)
        pygame.display.flip()    
        
        self.tiles = []
        self.screen.fill((200, 200, 200))

    def build_map(self, *blocks):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                x_coord, y_coord = j * self.block_size - self.camera.x, i * self.block_size - self.camera.y
                cur_block = self.blocks.get(self.map[i][j])
                if cur_block is not None:
                    self.screen.blit(cur_block, (x_coord, y_coord))
                    self.tiles.append(pygame.Rect(x_coord, y_coord, self.block_size, self.block_size))
    
    def load_level(self, level):
        self.level = level
