from physics import *
from camera import *
from game_objects import *
from field import *

import pygame


pygame.init()

game_map = [ ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'] ]


TILE_SIZE = 50

WIN_SIZE = (TILE_SIZE * 12, TILE_SIZE * 8)
OFFSET = (50, 50)

wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall.fill((200, 0, 0))
wall_rect = wall.get_rect()

field = Field(pygame.display.set_mode(WIN_SIZE), game_map, {'1' : wall}, TILE_SIZE, Player('player.png', (TILE_SIZE//2, TILE_SIZE//2), 100, 0, 100))
field.player.set_transparent_color((255, 255, 255))
field.player.rect = field.player.rect.move(max(TILE_SIZE, field.camera.x + field.camera.offset_w), max(TILE_SIZE, field.camera.y + field.camera.offset_h))

clock = pygame.time.Clock()


running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    field.build_map()

    field.player.move(field.tiles)
        
    field.update()

    clock.tick(60)               
    
pygame.display.quit()
pygame.quit()
