class Physics():
    def __init__(self, applied_force = 1, gravity = 0.4, friction_coeff = 0.15):
        self.gravity = gravity
        self.friction_coeff = friction_coeff
        self.force = applied_force
        self.velocity = [0, 0]
        self.collides = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        
    def update(self):
        self.velocity[1] += self.gravity

        if self.collides['down']:
            self.velocity[0] *= (1 - self.friction_coeff)
        else:
            self.velocity[0] *= (1 - self.friction_coeff/10)

        if self.collides['down']:
            self.velocity[1] = 0
        if self.collides['up']:
            self.velocity[1] = 0
        if self.collides['left']:
            self.velocity[0] = 0
        if self.collides['right']:
            self.velocity[0] = 0
