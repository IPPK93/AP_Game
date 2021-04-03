import pygame

class GameObject():
    def __init__(self, image, size):
        self.image = image
        self.width, self.height = size
        self.surf = pygame.image.load(image).convert()
        self.surf = pygame.transform.scale(self.surf, size)
        self.rect = self.surf.get_rect()
