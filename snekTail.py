from gameSprite import *


class SnekTail(GameSprite):
    def __init__(self, image, dimensions, position, controller_id, pause_timer, position_queue=[]):
        super(SnekTail, self).__init__(image, dimensions, position)
        self.controller_id = controller_id
        self.position_queue = []
        for i in range(pause_timer):
            self.position_queue.append(self.position)
        for p in position_queue:
            self.position_queue.append(p)

    def update(self):
        if self.position_queue:
            self.position = self.position_queue.pop(0)
        super(SnekTail, self).update()
