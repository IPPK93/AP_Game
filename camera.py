import pygame

# size = (width, height)
# offset = (offset_w, offset_h)
class Camera():
    def __init__(self, size, offset):
        self.rect = pygame.Rect((0, 0), size)
        self._offset_w, self._offset_h = offset
        
    def update(self, obj):
        dx, dy = 0, 0
        if self.rect.x + self.rect.width - self._offset_w < obj.right:
            dx = obj.right - (self.rect.x + self.rect.width - self._offset_w)
        if self.rect.x + self._offset_w > obj.left:
            dx = obj.left - (self.rect.x + self._offset_w)
        if self.rect.y + self._offset_h > obj.top:
            dy = obj.top - (self.rect.y + self._offset_h)
        if self.rect.y + self.rect.height - self._offset_h < obj.bottom:
            dy = obj.bottom - (self.rect.y + self.rect.height - self._offset_h)
        self.rect.x += dx
        self.rect.y += dy

    def get_xoffset(self):
        return self.rect.x + self._offset_w
    
    def get_yoffset(self):
        return self.rect.y + self._offset_h
     
    def get_offset(self):
        return (self.get_xoffset(), self.get_yoffset())