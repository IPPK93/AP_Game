import pygame

class Mouse():
    def __init__(self):
        self.pos = (-10000, -10000)
        self.collisions = []
        
    def update(self, offset):
        press = pygame.mouse.get_pressed()
        if press[0]:
            self.pos = tuple(map(sum, zip(pygame.mouse.get_pos(), offset)))
        else:
            self.pos = (-10000, -10000)
        
    def collides(self, group):
        self.collisions = []
        for elem in group:
            if elem.collidepoint(self.pos):
                self.collisions.append(elem)
