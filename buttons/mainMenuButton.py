from button import *


class MainMenuButton(Button):
    def __init__(self, position=(512, 475)):
        super(MainMenuButton, self).__init__("images/button_main_menu.png", (180, 36), 10,
                                              dimensions=(197, 50), position=position)
        self.needs_switch = False