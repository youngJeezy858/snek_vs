from button import *


class BackButton(Button):
    def __init__(self, position=(512, 475)):
        super(BackButton, self).__init__("images/button_back.png", (84, 36), 10,
                                         dimensions=(84, 50), position=position)
