import pygame

def move_player(player_rect, velocity, tiles):
    res = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
    player_rect.x += velocity[0]
    collisions = player_rect.collidelistall(tiles)
    for i in collisions:
        if velocity[0] > 0:
            player_rect.right = tiles[i].left
            res['right'] = True
        else: # velocity[0] < 0
            player_rect.left = tiles[i].right
            res['left'] = True
    player_rect.y += velocity[1]
    collisions = player_rect.collidelistall(tiles)
    for i in collisions:
        if velocity[1] > 0:
            player_rect.bottom = tiles[i].top
            res['down'] = True
        else: # velocity[1] < 0
            player_rect.top = tiles[i].bottom
            res['up'] = True
            
    return res

pygame.init()


TILE_SIZE = 50
STEP = 2

print(['0' for i in range(8)])

game_map = [ ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'] ]


clock = pygame.time.Clock()
screen = pygame.display.set_mode((TILE_SIZE * len(game_map[0]), TILE_SIZE * len(game_map)))


running = True

wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall.fill((200, 0, 0))

back = pygame.Surface((TILE_SIZE, TILE_SIZE))
back.fill((200, 200, 200))

wall_rect = wall.get_rect()
back_rect = back.get_rect()

player_surf = pygame.image.load('player.png').convert()
player_surf.set_colorkey((255, 255, 255))
player_surf = pygame.transform.scale(player_surf, (TILE_SIZE//2, TILE_SIZE//2))
player_rect = pygame.Rect(50, 100, player_surf.get_width(), player_surf.get_height())


player_velocity = [0, 0]
player_acceleration = [0., 0.]

while running:
    
    tiles = []
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                player_acceleration[0] += 1.
            if event.key == pygame.K_LEFT:
                player_acceleration[0] -= 1.
            if event.key == pygame.K_UP:
                player_acceleration[1] -= 1.
            if event.key == pygame.K_DOWN:
                player_acceleration[1] += 1.
    
    
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[i][j] == '1':
                screen.blit(wall, (j * TILE_SIZE, i * TILE_SIZE))
                tiles.append(pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif game_map[i][j] == '0':
                screen.blit(back, (j * TILE_SIZE, i * TILE_SIZE))
              
    collision = move_player(player_rect, player_velocity, tiles)
    
    if collision['down']:
        player_acceleration[1] = 0
        player_velocity[1] = 0
    else:
        player_acceleration[1] += 0.09
    if collision['up']:
        player_acceleration[1] = 0
        player_velocity[1] = 0
    if collision['left']:
        player_acceleration[0] = 0
        player_velocity[0] = 0
    if collision['right']:
        player_acceleration[0] = 0
        player_velocity[0] = 0
        
    player_velocity = [int(round(player_velocity[i] + player_acceleration[i])) for i in range(2)]
    player_acceleration[0] =  -0.49999999999999*player_velocity[0]

    
    screen.blit(player_surf, player_rect)
    pygame.display.flip()
    clock.tick(60)
    
pygame.display.quit()
pygame.quit()
