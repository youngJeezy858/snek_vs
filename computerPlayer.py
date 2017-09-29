from gameSprite import *
from pygame.locals import *
import math
from snekTail import *
from player import *


class ComputerPlayer(Player):

    def __init__(self, player_id, color, shade_id, dimensions, position, movement_speed):
        super(ComputerPlayer, self).__init__(player_id, color, shade_id, dimensions, position, -9999, movement_speed)

    def determine_movement(self, pellet, players, leftovers):
        # Find distance between self and pellet
        pellet_distance = math.sqrt(
            ((pellet.position[0] - self.real_x) * (pellet.position[0] - self.real_x)) +
            ((pellet.position[1] - self.real_y) * (pellet.position[1] - self.real_y))
        )
        d_ratio = self.movement_speed / pellet_distance
        x = float((1 - d_ratio) * self.real_x + (d_ratio * pellet.position[0]))
        y = float((1 - d_ratio) * self.real_y + (d_ratio * pellet.position[1]))
        self.x_add = x - self.real_x
        self.y_add = y - self.real_y
