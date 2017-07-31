from button import *


class OptionsGameButton(Button):
    def __init__(self):
        super(OptionsGameButton, self).__init__("images/button_options.png", (140, 36), 10,
                                                dimensions=(140, 50), position=(512, 425))
