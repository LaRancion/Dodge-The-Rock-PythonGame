
from utils import load_sprite

class GameObject:
    def __init__(self, position, velocity, sprite):
        self.position = position
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = velocity
        
    def draw(self, surface):
        blit_pos = self.position - self.radius
        surface.blit(self.sprite, blit_pos) # ?
    
    def move(self):
        self.position = self.position + self.velocity
    
    def collides_with(self, other_object):
        distance = self.position.distance_to(other_object.position)
        return distance < self.radius + other_object.radius
    
class Player(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("mario"))
        


class Ostacoli(GameObject):
    def __init__(self, position):
        super().__init__(position, load_sprite("tortuga"))