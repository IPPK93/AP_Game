from game_object import GameObject

class LifelessObject(GameObject):
    def __init__(self, image, size, destructibility):
        super().__init__(image, size)
        self.destructible = destructibility
        
class Block(LifelessObject):
    def __init__(self, image, size, destructibility):
        super().__init__(image, size, destructibility)
        

class StaticBlock(Block):
    def __init__(self, size, image = 'temp_block.png'):
        super().__init__(image, size, False)
        
    def get_moved_block(self, *position):
        new_block = StaticBlock((self.width, self.height), self.image)
        new_block.rect = new_block.rect.move(*position)
        return new_block
        
class GameItem(LifelessObject):
    def __init__(self, image, size):
        super().__init__(image, size, False)  
