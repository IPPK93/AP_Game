class Physics():
    def __init__(self, applied_force = 1, gravity = 0.4, friction_coeff = 0.15, air_friction_coeff = None, init_velocity = None, collide_react = None):
        self.gravity = gravity
        self.friction_coeff = friction_coeff
        self.air_friction_coeff = friction_coeff/10 if air_friction_coeff is None else air_friction_coeff
        self.force = applied_force
        self.velocity = [0, 0] if init_velocity is None else init_velocity
        self.collides = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.collide_react = self._st_col_react if collide_react is None else collide_react
        
    def _st_col_react(self, velocity, index):
        velocity[index] = 0
        
    def fix_friction(self):
        if self.collides['down']:
            self.velocity[0] *= (1 - self.friction_coeff)
        else:
            self.velocity[0] *= (1 - self.air_friction_coeff)
        
    def fix_gravity(self):
        self.velocity[1] += self.gravity
        
    def update(self):
        self.fix_gravity()
        self.fix_friction()
        
        if self.collides['down'] or self.collides['up']:
            self.collide_react(self.velocity, 1)
        if self.collides['left'] or self.collides['right']:
            self.collide_react(self.velocity, 0)
        
# applied_force = 1, gravity = 0.4, friction_coeff = 0.15,