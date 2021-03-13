from game_objects import *
from field import *
import pygame


pygame.init()

TILE_SIZE = 48

WIN_SIZE = (800, 600)
OFFSET = (50, 50)

# wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
# wall.fill((200, 0, 0))
# wall_rect = wall.get_rect()

field = Field(pygame.display.set_mode(WIN_SIZE), {'w' : StaticBlock((TILE_SIZE, TILE_SIZE))}, TILE_SIZE, Player('player.png', (TILE_SIZE//2, TILE_SIZE//2), 100, 0, 100))
field.load_map('maps/01.txt')

field.player.set_transparent_color((255, 255, 255))
field.player.rect = field.player.rect.move(field.camera.rect.x + field.camera.offset_w + 2* TILE_SIZE, field.camera.rect.y + field.camera.offset_h + TILE_SIZE)

clock = pygame.time.Clock()

field.enemies.append(Enemy('enemy_1.png', (TILE_SIZE//2, TILE_SIZE//2), 100, 0, 100))
field.enemies[-1].rect = field.enemies[-1].rect.move(field.camera.rect.x + field.camera.offset_w + TILE_SIZE, field.camera.rect.y + field.camera.offset_h + TILE_SIZE) 

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    field.update()
    
    clock.tick(60)
    
pygame.display.quit()
pygame.quit()
