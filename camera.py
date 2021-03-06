import pygame

# size = (width, height)
# offset = (offset_w, offset_h)
class Camera():
    def __init__(self, size, offset):
        self.rect = pygame.Rect((0, 0), size)
        self.offset_w, self.offset_h = offset
        
    def update(self, obj_rect):
        dx, dy = 0, 0
        if self.rect.x + self.rect.width - self.offset_w < obj_rect.right:
            dx = obj_rect.right - (self.rect.x + self.rect.width - self.offset_w)
        if self.rect.x + self.offset_w > obj_rect.left:
            dx = obj_rect.left - (self.rect.x + self.offset_w)
        if self.rect.y + self.offset_h > obj_rect.top:
            dy = obj_rect.top - (self.rect.y + self.offset_h)
        if self.rect.y + self.rect.height - self.offset_h < obj_rect.bottom:
            dy = obj_rect.bottom - (self.rect.y + self.rect.height - self.offset_h)
        self.rect.x += dx
        self.rect.y += dy
