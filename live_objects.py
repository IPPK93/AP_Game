import pygame
from physics import *
from game_object import GameObject
from lifeless_objects import *
from constants import Constant

class LiveObject(GameObject):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, init_pos = (0, 0), physics = Physics()):
        super().__init__(image, size, init_pos)
        self.physics = physics
        self.image_direction = 1
    
    def update(self):
        self.physics.update()
        
        if self.image_direction * self.physics.x_vel < 0:
            self.surf = pygame.transform.flip(self.surf, True, False)
            self.image_direction *= -1
    
    def move(self, *group):
        res = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        velocity = tuple(map(round, self.physics.velocity))
        obstacles = list(map(lambda obj: obj.rect, group))
        
        self.x += velocity[0]
        collisions = self.rect.collidelistall(obstacles)
        for i in collisions:
            if isinstance(i, DynamicBlock):
                i.react_func()
            if velocity[0] > 0:
                self.right = obstacles[i].left
                res['right'] = True
            elif velocity[0] < 0:
                self.left = obstacles[i].right
                res['left'] = True

        self.y += velocity[1]
        collisions = self.rect.collidelistall(obstacles)
        for i in collisions:
            if velocity[1] > 0:
                self.bottom = obstacles[i].top
                res['down'] = True
            elif velocity[1] < 0:
                self.top = obstacles[i].bottom
                res['up'] = True

        setattr(self.physics, 'collides', res)

class Enemy(LiveObject):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, init_pos = (0, 0), physics = None):
        if physics is None:
            physics = Physics1(init_velocity = [1, 0], applied_force = 1)
        super().__init__(image, size, init_pos, physics)
        
    def move(self, *obstacles):
        super().move(*obstacles)
        self.ai_move()

    def ai_move(self):
        self.physics.nullify_friction_effect()

        
class Player(LiveObject):
    def __init__(self, image, size = Constant.PLAYER_SIZE, init_pos = (0, 0), physics = Physics()):
        super().__init__(image, size, init_pos, physics)
        self.air_time = 0
        
    def move(self, *obstacles):
        pressed = pygame.key.get_pressed()
            
        direction = complex(pressed[pygame.K_RIGHT] - pressed[pygame.K_LEFT], -pressed[pygame.K_UP])

        self.physics.apply_force(direction)
        
        super().move(*obstacles)

class NoGravityGuy(Enemy):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, init_pos = (0, 0), physics = Physics(0, 0, 0, init_velocity = [5, 0])):
        super().__init__(image, size, init_pos, physics)
        self.step_counter = 0
        self.step_limit = 48 * 5
        self.cur_direction = 'right'
        
    def collide_react(self, velocity, index):
        velocity[index] *= -1
    
    def ai_move(self):
        self.step_counter += abs(self.physics.x_vel)
        
        if self.step_counter == self.step_limit or self.physics.collides['right'] or self.physics.collides['left']:
            self.physics.set_collision(self.cur_direction)
            if self.cur_direction == 'right':
                self.cur_direction = 'left'
            else:
                self.cur_direction = 'right'
            
            self.step_counter = 0
        
class MovingGuy(Enemy):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, init_pos = (0, 0), target = None, physics = None):
        if physics is None:
            physics = Physics(applied_force = 0.1, gravity = 0, friction_coeff = 0)
        super().__init__(image, size, init_pos, physics)
        self.act_radius_sqr = Constant.DEFAULT_ACT_RADIUS ** 2
        self.target = target
        
    def ai_move(self):
        if (self.x - self.target.x) ** 2 + (self.y - self.target.y) ** 2 <= self.act_radius_sqr:
            direction = complex(-1 if self.target.right < self.left else 1, -1 if self.target.top < self.bottom else 1)
            self.physics.apply_force(direction)