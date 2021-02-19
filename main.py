import pygame

def move_player(player_rect, velocity, tiles):
    res = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
    player_rect.x += velocity[0]
    collisions = player_rect.collidelistall(tiles)
    for i in collisions:
        if velocity[0] > 0:
            player_rect.right = tiles[i].left
            res['right'] = True
        elif velocity[0] < 0:
            player_rect.left = tiles[i].right
            res['left'] = True
    
    player_rect.y += velocity[1]
    collisions = player_rect.collidelistall(tiles)
    for i in collisions:
        if velocity[1] > 0:
            player_rect.bottom = tiles[i].top
            res['down'] = True
        elif velocity[1] < 0:
            player_rect.top = tiles[i].bottom
            res['up'] = True
            
    return res

pygame.init()

game_map = [ ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'] ]

TILE_SIZE = 50
STEP = 2

WIN_SIZE_X, WIN_SIZE_Y = TILE_SIZE * len(game_map[0]), TILE_SIZE * len(game_map) # TILE_SIZE * 12, TILE_SIZE * 11



clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))


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

# scroll = [0, 0]

while running:
    
    screen.fill((200, 200, 200))
    
    tiles = []
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                player_velocity[0] += 3
            if event.key == pygame.K_LEFT:
                player_velocity[0] -= 3
            if event.key == pygame.K_UP:
                player_velocity[1] -= 5
    
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            x_coord, y_coord = j * TILE_SIZE, i * TILE_SIZE
            if game_map[i][j] == '1':
                screen.blit(wall, (x_coord, y_coord))
                tiles.append(pygame.Rect(x_coord, y_coord, TILE_SIZE, TILE_SIZE))
            elif game_map[i][j] == '0':
                screen.blit(back, (x_coord, y_coord))
    
#     scroll[0] -= player_rect.x
#     scroll[1] -= player_rect.y
    
    collision = move_player(player_rect, list(map(round, player_velocity)), tiles)
    
#     scroll[0] += player_rect.x
#     scroll[1] += player_rect.y
    
    if collision['down']:
        player_velocity[0] *= 0.85
    else:
        player_velocity[0] *= 0.99

    player_velocity[1] += 0.8
    
    if collision['down']:
        player_velocity[1] = 0
    if collision['up']:
        player_velocity[1] = 0
    if collision['left']:
        player_velocity[0] = 0
    if collision['right']:
        player_velocity[0] = 0
        
    

    screen.blit(player_surf, player_rect)
    pygame.display.flip()
    clock.tick(60)
    print(f'Velocity: {player_velocity}')
#     print('scroll: ', scroll)
    
pygame.display.quit()
pygame.quit()
