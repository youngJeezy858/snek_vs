from button import *


class PlayAgainButton(Button):
    def __init__(self, position=(512, 425)):
        super(PlayAgainButton, self).__init__("images/button_play_again.png", (185, 36), 10,
                                              dimensions=(200, 50), position=position)
        self.needs_switch = False
