from gameSprite import *
from random import randint
from logger import *
from constants.debugging_flags import *

class Pellet(GameSprite):
    def __init__(self, image, dimensions, upper_x, upper_y):
        self.logger = Logger("pellet", DEBUG_PELLET)
        self.position = (0, 0)
        super(Pellet, self).__init__(image, dimensions, self.position)
        self.reset_position(upper_x, upper_y)

    def reset_position(self, width, height):
        lower_x = self.dimensions[0]/2
        upper_x = width - self.dimensions[0]/2
        lower_y = self.dimensions[1]/2
        upper_y = height - self.dimensions[1]/2
        self.logger.debug("reset position", "x: [%s - %s], y: [%s, %s]" % (lower_x, upper_x, lower_y, upper_y))
        self.position = (randint(lower_x, upper_x), randint(lower_y, upper_y))
        self.rect.center = self.position
