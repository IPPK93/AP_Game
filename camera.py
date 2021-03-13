import pygame

# size = (width, height)
# offset = (offset_w, offset_h)
class Camera():
    def __init__(self, size, offset):
        self.rect = pygame.Rect((0, 0), size)
        self.offset_w, self.offset_h = offset
        
    def update(self, obj):
        dx, dy = 0, 0
        if self.rect.x + self.rect.width - self.offset_w < obj.rect.right:
            dx = obj.rect.right - (self.rect.x + self.rect.width - self.offset_w)
        if self.rect.x + self.offset_w > obj.rect.left:
            dx = obj.rect.left - (self.rect.x + self.offset_w)
        if self.rect.y + self.offset_h > obj.rect.top:
            dy = obj.rect.top - (self.rect.y + self.offset_h)
        if self.rect.y + self.rect.height - self.offset_h < obj.rect.bottom:
            dy = obj.rect.bottom - (self.rect.y + self.rect.height - self.offset_h)
        self.rect.x += dx
        self.rect.y += dy
