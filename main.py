from live_objects import *
from lifeless_objects import *
from field import *
from constants import Constant
import pygame

pygame.init()
clock = pygame.time.Clock()
    
disp = pygame.display.set_mode(Constant.WIN_SIZE)
field = Field(disp, Player('sprites/live_objects/Wizard_Idle.png', Constant.PLAYER_SIZE, init_pos = (5 * Constant.TILE_SIZE, 5 * Constant.TILE_SIZE)))

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    field.update()
    
    clock.tick(Constant.FPS)
    
pygame.display.quit()
pygame.quit()
