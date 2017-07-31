from button import *
import sys


class QuitGameButton(Button):
    def __init__(self):
        super(QuitGameButton, self).__init__("images/button_quit.png", (78, 36), 10,
                                             dimensions=(78, 50), position=(512, 475))

    def update(self):
        super(QuitGameButton, self).update()
        if self.state == self.ACTIVE:
            print "I'm going to sleep..."
            pygame.quit()
            sys.exit()
