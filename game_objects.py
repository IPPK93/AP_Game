from physics import *
import pygame

class GameObject():
    def __init__(self, image, size):
        self.image = image
        self.width, self.height = size
        self.surf = pygame.image.load(image).convert()
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect()
        
class LiveObject(GameObject):
    def __init__(self, image, size, hp, damage, mp, init_items = []):
        super().__init__(image, size)
        self.hp = hp
        self.damage = damage
        self.mp = mp
        self.items = init_items
        self.physics = Physics()
        self.velocity = self.physics.velocity
    
    def update(self):
        self.physics.update()
        
    def set_transparent_color(self, color):
        self.surf.set_colorkey(color)
        self.rect = self.surf.get_rect()
    
    def move(self, *group):
        res = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        velocity = tuple(map(round, self.physics.velocity))
        obstacles = list(map(lambda obj: obj.rect, group))
        
        self.rect.x += velocity[0]
        
        collisions = self.rect.collidelistall(obstacles)
        for i in collisions:
            if velocity[0] > 0:
                self.rect.right = obstacles[i].left
                res['right'] = True
            elif velocity[0] < 0:
                self.rect.left = obstacles[i].right
                res['left'] = True

        self.rect.y += velocity[1]
        collisions = self.rect.collidelistall(obstacles)
        for i in collisions:
            if velocity[1] > 0:
                self.rect.bottom = obstacles[i].top
                res['down'] = True
            elif velocity[1] < 0:
                self.rect.top = obstacles[i].bottom
                res['up'] = True

        self.physics.collides = res

class Enemy(LiveObject):
    def __init__(self, image, size, hp, damage, mp, init_items = []):
        super().__init__(image, size, hp, damage, mp, init_items)
        self.cur_direction = 'right'
        
    def move(self, *obstacles):
        super().move(*obstacles)
        self.ai_move()

    def ai_move(self):
        if self.physics.collides['right']:
            self.cur_direction = 'left'
        if self.physics.collides['left']:
            self.cur_direction = 'right'
        if self.cur_direction == 'left':
            self.velocity[0] -= self.physics.friction_coeff
        else:
            self.velocity[0] += self.physics.friction_coeff
            
        
class Player(LiveObject):
    def __init__(self, image, size, hp, damage, mp, init_items = []):
        super().__init__(image, size, hp, damage, mp, init_items)
        
    def move(self, *obstacles):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.velocity[1] -= self.physics.force
        if pressed[pygame.K_RIGHT]:
            self.velocity[0] += self.physics.force
        if pressed[pygame.K_LEFT]:
            self.velocity[0] -= self.physics.force
        
        super().move(*obstacles)

class LifelessObject(GameObject):
    def __init__(self, image, size, destructibility):
        super().__init__(image, size)
        self.destructible = destructibility
        
class Block(LifelessObject):
    def __init__(self, image, size, destructibility):
        super().__init__(image, size, destructibility)
        

class StaticBlock(Block):
    def __init__(self, size, image = 'temp_block.png'):
        super().__init__(image, size, False)
        
    def get_moved_block(self, *position):
        new_block = StaticBlock((self.width, self.height), self.image)
        new_block.rect = new_block.rect.move(*position)
        return new_block
        
class GameItem(LifelessObject):
    def __init__(self, image, size):
        super().__init__(image, size, False)        
