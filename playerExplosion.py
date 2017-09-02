from gameSprite import *
from pygame.locals import *
import random
import math
from snekTail import *
from logger import *
from constants.debugging_flags import *


class PlayerExplosion(GameSprite):

    # Clean up states
    PROCESSING = 0
    CLEAN_UP = 1

    def __init__(self, player, y_bound):
        self.logger = Logger("Player explosion", DEBUG_PLAYER_EXPLOSION)
        dimensions = player.dimensions[0] / 5, player.dimensions[1] / 3
        super(PlayerExplosion, self).__init__(player.image_path, dimensions, player.position)
        self.real_x = float(player.position[0])
        self.real_y = float(player.position[1])
        self.x_add = 0
        self.y_add = 0
        self.y_bound = y_bound
        self.state = self.PROCESSING
        self.movement_speed = player.movement_speed / 5
        self.explosion_degree = self.gen_explosion_degree()
        self.quadratic_a = random.uniform(0.1, 0.3)
        if self.explosion_degree > 0:
            self.movement_speed *= -1.0

    def update(self):
        if self.real_y + self.y_add + (self.dimensions[1] / 2) > self.y_bound:
            self.state = self.CLEAN_UP
        else:
            self.x_add, self.y_add = self.process_explosion()
            self.position = (self.real_x + self.x_add, self.real_y + self.y_add)
        super(PlayerExplosion, self).update()

    def gen_explosion_degree(self):
        degree = random.uniform(self.movement_speed * 5, self.movement_speed * 10) * random.choice([-1.0, 1.0])
        self.logger.debug("gen_explosion_degree", "explosion_degree = %s" % degree)
        return degree

    def process_explosion(self):
        self.logger.debug("gen_explosion_degree", "[x_add=%s, y_add=%s]" % (self.x_add, self.y_add))
        x = self.movement_speed + self.x_add
        y = (self.quadratic_a * x * x) + (self.explosion_degree * x)
        return x, y
