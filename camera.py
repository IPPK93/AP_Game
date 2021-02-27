# size = (width, height)
# offset = (offset_w, offset_h)
class Camera():
    def __init__(self, size, offset):
        self.width, self.height = size
        self.offset_w, self.offset_h = offset
        self.x, self.y = (0, 0)
        
    def update(self, player_rect):
        dx, dy = 0, 0
        if self.width - self.offset_w < player_rect.right:
            dx = player_rect.right - (self.width - self.offset_w)
        if self.offset_w > player_rect.left:
            dx = player_rect.left - self.offset_w
        if self.offset_h > player_rect.top:
            dy = player_rect.top - self.offset_h
        if self.height - self.offset_h < player_rect.bottom:
            dy = player_rect.bottom - (self.height - self.offset_h)
        self.x += dx
        self.y += dy
        player_rect.x -= dx
        player_rect.y -= dy
