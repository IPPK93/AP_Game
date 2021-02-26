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

WIN_SIZE_X, WIN_SIZE_Y = TILE_SIZE * 12, TILE_SIZE * 8 # TILE_SIZE * len(game_map[0]), TILE_SIZE * len(game_map)



clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIN_SIZE_X, WIN_SIZE_Y))


running = True

wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
wall.fill((200, 0, 0))

back = pygame.Surface((TILE_SIZE, TILE_SIZE))
back.fill((200, 200, 200))

wall_rect = wall.get_rect()
back_rect = back.get_rect()


camera = [0, 0]
offset_x, offset_y = 50, 50

player_surf = pygame.image.load('player.png').convert()
player_surf.set_colorkey((255, 255, 255))
player_surf = pygame.transform.scale(player_surf, (TILE_SIZE//2, TILE_SIZE//2))
player_rect = pygame.Rect(max(TILE_SIZE, camera[0] + offset_x), max(TILE_SIZE, camera[1] + offset_y), player_surf.get_width(), player_surf.get_height())


player_velocity = [0, 0]

move = {'right' : False, 'left' : False, 'up' : False}

camera_x, camera_y = 0, 0

while running:
    
    screen.fill((200, 200, 200))
    
    tiles = []
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    pressed = pygame.key.get_pressed()
    
    if pressed[pygame.K_UP]:
        player_velocity[1] -= 1
    if pressed[pygame.K_RIGHT]:
        player_velocity[0] += 1
    if pressed[pygame.K_LEFT]:
        player_velocity[0] -= 1
                
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            x_coord, y_coord = j * TILE_SIZE - camera[0], i * TILE_SIZE - camera[1]
            if game_map[i][j] == '1':
                screen.blit(wall, (x_coord, y_coord))
                tiles.append(pygame.Rect(x_coord, y_coord, TILE_SIZE, TILE_SIZE))
            elif game_map[i][j] == '0':
                screen.blit(back, (x_coord, y_coord))
               
            
            
    collision = move_player(player_rect, list(map(round, player_velocity)), tiles)
    
    
#     print(f"WIN_SIZE_X - offset_x: {WIN_SIZE_X - offset_x}")
#     print(f"player_rect.right: {player_rect.right}")
#     print(f"offset_x: {offset_x}")
#     print(f"player_rect.left: {player_rect.left}")
#     print()
#     print(f"offset_y: {offset_y}")
#     print(f"player_rect.top: {player_rect.top}")
#     print(f"WIN_SIZE_Y - offset_y: {WIN_SIZE_Y - offset_y}")
#     print(f"player_rect.bottom: {player_rect.bottom}")
#     print()
    
    if WIN_SIZE_X - offset_x < player_rect.right:
        camera_x = player_rect.right - (WIN_SIZE_X - offset_x)
    if offset_x > player_rect.left:
        camera_x = player_rect.left - offset_x
    if offset_y > player_rect.top:
        camera_y = player_rect.top - offset_y
    if WIN_SIZE_Y - offset_y < player_rect.bottom:
        camera_y = player_rect.bottom - (WIN_SIZE_Y - offset_y)

    
    if collision['down']:
        player_velocity[0] *= 0.85
    else:
        player_velocity[0] *= 0.99

    player_velocity[1] += 0.4
    
    if collision['down']:
        player_velocity[1] = 0
    if collision['up']:
        player_velocity[1] = 0
    if collision['left']:
        player_velocity[0] = 0
    if collision['right']:
        player_velocity[0] = 0
        
    camera[0] += camera_x
    player_rect.x -= camera_x
    camera[1] += camera_y
    player_rect.y -= camera_y
    camera_x = 0
    camera_y = 0
    
    screen.blit(player_surf, player_rect)
    pygame.display.flip()
    clock.tick(60)
#     print(f'Velocity: {player_velocity}')
    
pygame.display.quit()
pygame.quit()
