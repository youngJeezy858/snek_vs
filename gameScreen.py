from abc import *
import pygame
from controller import *


class GameScreen(object):

    START_MENU = 0
    SOLO_GAME = 1

    CONTROLLER_EVENTS = (
        JOYAXISMOTION,
        JOYBALLMOTION,
        JOYHATMOTION,
        JOYBUTTONUP,
        JOYBUTTONDOWN
    )
    MOUSE_KEY_EVENTS = (
        KEYDOWN,
        KEYUP,
        MOUSEMOTION,
        MOUSEBUTTONUP,
        MOUSEBUTTONDOWN
    )

    def __init__(self, screen):
        self.screen = screen
        self.MIN_WIDTH = 1024
        self.MIN_HEIGHT = 576
        self.needs_switch = False
        self.needs_resize = False
        self.controllers = []
        self.active_controller = False
        self.check_for_controllers()

    def calculate_dimensions(self, (width, height)):
        expanded_width = float(width) * float(self.width) / float(self.MIN_WIDTH)
        expanded_height = float(height) * float(self.height) / float(self.MIN_HEIGHT)
        rounded_width = int(round(expanded_width))
        rounded_height = int(round(expanded_height))
        return rounded_width, rounded_height

    def calculate_position(self, (x, y)):
        expanded_x = float(self.width) / float(self.MIN_WIDTH) * float(x)
        expanded_y = float(self.height) / float(self.MIN_HEIGHT) * float(y)
        rounded_x = int(round(expanded_x))
        rounded_y = int(round(expanded_y))
        return rounded_x, rounded_y

    @abstractmethod
    def next_screen(self):
        return

    @abstractmethod
    def check_event(self, event):
        return

    @abstractmethod
    def update(self):
        return

    @abstractmethod
    def resize_screen(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

    def is_controller_active(self, event):
        if event.type in self.CONTROLLER_EVENTS:
            return True
        else:
            return False

    def check_for_controllers(self):
        joysticks = pygame.joystick.get_count()
        for i in range(joysticks):
            self.active_controller = True
            self.controllers.append(Controller(pygame.joystick.Joystick(i)))
