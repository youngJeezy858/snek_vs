from button import *
from static_classes.screenResizer import *
from constants.window_constants import *


class FullscreenGameButton(Button):
    def __init__(self, full_screen=False):
        self.full_screen_image = "images/button_fullscreen.png"
        self.windowed_image = "images/button_windowed.png"
        self.full_screen = full_screen
        super(FullscreenGameButton, self).__init__(self.full_screen_image, (256, 36), 10,
                                                   dimensions=(256, 50), position=(512, 425))
        if not self.full_screen:
            self.sprite_sheet_master = pygame.image.load(self.windowed_image)
            self.set_image(self.current_sprite)

    def flip_screen_mode(self, screen):
        if self.full_screen:
            self.sprite_sheet_master = pygame.image.load(self.windowed_image)
            self.full_screen = False
            self.state = self.INACTIVE
            ScreenResizer.resize_screen(screen, (WINDOW_SIZE[0], WINDOW_SIZE[1]))
        else:
            self.sprite_sheet_master = pygame.image.load(self.full_screen_image)
            self.full_screen = True
            self.state = self.INACTIVE
            ScreenResizer.full_screen(screen)
        self.set_image(self.current_sprite)
