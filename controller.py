from pygame.locals import *


class Controller(object):

    def __init__(self, joystick):
        joystick.init()
        self.controller = joystick

    def check_event(self, event):
        if event.type == JOYAXISMOTION and event.joy == self.controller.get_id():
            self.calculate_joyaxismotion(event)
        elif event.type == JOYBUTTONDOWN and event.joy == self.controller.get_id():
            self.calculate_joybuttondown(event)
        elif event.type == JOYBUTTONUP and event.joy == self.controller.get_id():
            self.calculate_joybuttonup(event)
        elif event.type == JOYBALLMOTION and event.joy == self.controller.get_id():
            self.calculate_joyballmotion(event)
        elif event.type == JOYHATMOTION and event.joy == self.controller.get_id():
            self.calculate_joyhatmotion(event)

    def calculate_joyaxismotion(self, event):
        msg = ['axismotion', event.joy, event.axis, event.value]
        print msg
        # # Left thumb stick
        # if event.axis == 0:
        #     if abs(event.value) < 0.1:
        #         self.player.x_add = 0
        #     else:
        #         self.player.x_add = event.value
        # elif event.axis == 1:
        #     if abs(event.value) < 0.2:
        #         self.player.y_add = 0
        #     else:
        #         self.player.y_add = event.value
        #
        # # Right thumb stick
        # elif event.axis == 3:
        #     if abs(event.value) > 0.1:
        #         self.player.y_look = event.value
        #         self.player.shield_up = True
        #     else:
        #         self.player.y_look = 0
        # elif event.axis == 4:
        #     if abs(event.value) > 0.1:
        #         self.player.x_look = event.value
        #         self.player.shield_up = True
        #     else:
        #         self.player.x_look = 0
        # else:
        #     self.player.shield_up = False

    def calculate_joybuttonup(self, event):
        msg = ['button', event.joy, event.button, 0]
        print msg

    def calculate_joybuttondown(self, event):
        msg = ['button', event.joy, event.button, 1]
        print msg

    def calculate_joyballmotion(self, event):
        msg = ['ballmotion', event.joy, event.ball, event.value]
        print msg

    def calculate_joyhatmotion(self, event):
        msg = ['hatmotion', event.joy, event.hat, event.value[0], event.value[1]]
        print msg