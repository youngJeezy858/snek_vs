from button import *


class StartGameButton(Button):
    def __init__(self):
        super(StartGameButton, self).__init__("images/button_start.png", (100, 36), 10,
                                              dimensions=(100, 50), position=(512, 375))
        self.needs_switch = False

    def update(self):
        super(StartGameButton, self).update()
        if self.state == self.ACTIVE:
            self.needs_switch = True
            print "Start the game already!"
