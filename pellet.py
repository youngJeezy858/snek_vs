from gameSprite import *
from random import randint


class Pellet(GameSprite):
    def __init__(self, image, dimensions, position):
        super(Pellet, self).__init__(image, dimensions, position)

    def reset_position(self, width, height):
        self.position = (randint(self.dimensions[0]/2, width - self.dimensions[0]/2),
                         randint(self.dimensions[1]/2, height - self.dimensions[1]/2))
