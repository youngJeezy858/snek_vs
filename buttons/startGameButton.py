from button import *


class StartGameButton(Button):
    def __init__(self, position=(512, 425)):
        super(StartGameButton, self).__init__("images/button_start.png", (100, 36), 10,
                                              dimensions=(100, 50), position=position)
        self.needs_switch = False
