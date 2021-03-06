from game_object import GameObject
from copy import copy
from constants import Constant

class LifelessObject(GameObject):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, destructibility = False):
        super().__init__(image, size)
        self.destructible = destructibility

class Block(LifelessObject):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, destructibility = False):
        super().__init__(image, size, destructibility)
        
    def get_moved_block(self, *position):
        new_block = copy(self)
        new_block.rect = new_block.rect.move(*position)
        return new_block

class StaticBlock(Block):
    def __init__(self, image, size = Constant.DEFAULT_SIZE):
        super().__init__(image, size, False)
        self.surf.set_colorkey('white')
        
class DynamicBlock(Block):
    def __init__(self, image, size = Constant.DEFAULT_SIZE, destructibility = False, move_limit = Constant.MOVE_LIMIT):
        super().__init__(image, size, destructibility)
        self.move_counter = 0
        self.move_limit = move_limit
        self.move_right = True
        
    def move(self, *group):
        self.rect.x += self.move_right - (not self.move_right)
        self.move_counter += 1
        self.move_counter %= self.move_limit
        if self.move_counter == 0:
            self.move_right = not self.move_right