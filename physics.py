from abc import ABC, abstractmethod
from math import copysign

class AbstractPhysics(ABC):

    @property
    @abstractmethod
    def gravity(self):
        pass
    
    @gravity.setter
    @abstractmethod
    def gravity(self, val):
        pass
    
    @property
    @abstractmethod
    def friction_coeff(self):
        pass
    
    @friction_coeff.setter
    @abstractmethod
    def friction_coeff(self, val):
        pass

    @property
    @abstractmethod
    def force(self):
        pass
    
    @force.setter
    @abstractmethod
    def force(self, val):
        pass
    
    @property
    @abstractmethod
    def velocity(self):
        pass
    
    @velocity.setter
    @abstractmethod
    def velocity(self, val):
        pass
    
    @property
    @abstractmethod
    def collides(self):
        pass
    
    @collides.setter
    @abstractmethod
    def collides(self, val):
        pass    
    
    @classmethod
    @abstractmethod
    def collide_react(self, axis_index):
        pass
    
    @classmethod
    @abstractmethod
    def fix_friction(self):
        pass
    
    @classmethod
    @abstractmethod
    def fix_gravity(self):
        pass
        
    @classmethod
    @abstractmethod
    def update(self):
        pass

class Physics(AbstractPhysics):
    def __init__(self, applied_force = 1, gravity = 0.4, friction_coeff = 0.15, air_friction_coeff = None, init_velocity = None):
        super().__init__()
        self._gravity = gravity
        self._friction_coeff = friction_coeff
        self._air_friction_coeff = friction_coeff/10 if air_friction_coeff is None else air_friction_coeff
        self._force = applied_force
        self._velocity = [0, 0] if init_velocity is None else init_velocity
        self._collides = {'up' : False, 'down' : False, 'left' : False, 'right' : False}

    def collide_react(self, axis_index):
        self._velocity[axis_index] = 0
        
    def fix_friction(self):
        if self._collides['down']:
            self._velocity[0] *= (1 - self._friction_coeff)
        else:
            self._velocity[0] *= (1 - self._air_friction_coeff)
        
    def fix_gravity(self):
        self._velocity[1] += self._gravity
        
    def apply_force(self, direction: complex):
        self._velocity[0] += direction.real * self._force
        self._velocity[1] += direction.imag * self._force    
    
    def nullify_friction_effect(self):
        if self._collides['down']:
            self._velocity[0] /= (1 - self._friction_coeff)
        else:
            self._velocity[0] /= (1 - self._air_friction_coeff)

    def update(self):
        self.fix_gravity()
        self.fix_friction()
        
        if self._collides['down'] or self._collides['up']:
            self.collide_react(1)
        if self._collides['left'] or self._collides['right']:
            self.collide_react(0)
            
    def set_collision(*directions):
        for direction in directions:
            self._collides[direction] = True
    
    @property
    def gravity(self):
        return self._gravity
    
    @gravity.setter
    def gravity(self, val):
        self._gravity = val
    
    @property
    def friction_coeff(self):
        return self._friction_coeff
    
    @friction_coeff.setter
    def friction_coeff(self, val):
        self._friction_coeff = val
    
    @property
    def force(self):
        return self._force
    
    @force.setter
    def force(self, val):
        self._force = val
    
    @property
    def velocity(self):
        return self._velocity
    
    @velocity.setter
    def velocity(self, val):
        self._velocity = val
    
    @property
    def collides(self):
        return self._collides
    
    @collides.setter
    def collides(self, val):
        self._collides = val
        
    @property
    def x_vel(self):
        return self._velocity[0]
    
    @x_vel.setter
    def x_vel(self, val):
        self._velocity[0] = val  
    
    @property
    def y_vel(self):
        return self._velocity[1]
    
    @y_vel.setter
    def y_vel(self, val):
        self._velocity[1] = val
    

class Physics1(Physics):
    def __init__(self, applied_force = 1, gravity = 0.4, friction_coeff = 0.15, air_friction_coeff = None, init_velocity = None):
        super().__init__(applied_force, gravity, friction_coeff, air_friction_coeff, init_velocity)
    
    def collide_react(self, axis_index):
        if axis == 1:
            super().collide_react(axis_index)
        else:
            self._velocity[axis_index] = copysign(1, self._velocity[axis_index]) * (-self._force)        

        
# applied_force = 1, gravity = 0.4, friction_coeff = 0.15