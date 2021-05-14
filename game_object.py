import pygame

class GameObject():
    def __init__(self, image, size):
        self.image = image
        self.width, self.height = size
        self.surf = pygame.image.load(image).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect()

    @property
    def right(self):
        return self.rect.right
    
    @right.setter
    def right(self, val):
        self.rect.right = val
        
    @property
    def left(self):
        return self.rect.left
    
    @left.setter
    def left(self, val):
        self.rect.left = val
    
    @property
    def top(self):
        return self.rect.top
    
    @top.setter
    def top(self, val):
        self.rect.top = val
    
    @property
    def bottom(self):
        return self.rect.bottom
    
    @bottom.setter
    def bottom(self, val):
        self.rect.bottom = val
        
    @property
    def x(self):
        return self.rect.x
    
    @x.setter
    def x(self, val):
        self.rect.x = val
        
    @property
    def y(self):
        return self.rect.y
    
    @y.setter
    def y(self, val):
        self.rect.y = val
