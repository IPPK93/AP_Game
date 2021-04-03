import pygame
from physics import *
from game_object import GameObject


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
    
    def set_physics(self, physics):
        self.physics = physics
        self.velocity = self.physics.velocity
    
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

class NoGravityGuy(Enemy):
    def __init__(self, image, size, hp, damage, mp, init_items = []):
        super().__init__(image, size, hp, damage, mp, init_items)
        self.set_physics(Physics(0, 0, 0, init_velocity = [5, 0], collide_react = self.collide_react))
        self.step_counter = 0
        self.step_limit = 48 * 5
        
    def collide_react(self, velocity, index):
        velocity[index] *= -1
    
    def ai_move(self):
        self.step_counter += abs(self.velocity[0])
        
        if self.step_counter == self.step_limit or self.physics.collides['right'] or self.physics.collides['left']:
            if self.cur_direction == 'right':
                self.physics.collides['right'] = True
                self.cur_direction = 'left'
            else:
                self.physics.collides['left'] = True
                self.cur_direction = 'right'
            
            self.step_counter = 0
        
class MovingGuy(Enemy):
    def __init__(self, image, size, hp, damage, mp, target, init_items = []):
        super().__init__(image, size, hp, damage, mp, init_items)
        self.set_physics(Physics(0.1, 0, 0, init_velocity = [5, 0], collide_react = None))
        self.act_radius_sqr = (48 * 10) ** 2
        del self.cur_direction
        self.target = target
        
    def ai_move(self):
        if (self.rect.x - self.target.rect.x) ** 2 + (self.rect.y - self.target.rect.y) ** 2 <= self.act_radius_sqr:
            if self.target.rect.right < self.rect.left:
                self.velocity[0] -= self.physics.force
            else:
                self.velocity[0] += self.physics.force
            if self.target.rect.top < self.rect.bottom:
                self.velocity[1] -= self.physics.force
            else:
                self.velocity[1] += self.physics.force