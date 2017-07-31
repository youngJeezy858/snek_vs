import pygame
import re
from pygame.locals import *
from screeninfo import get_monitors


class ScreenResizer(object):
    @staticmethod
    def check_event(game_screen, event):
        if event.type == VIDEORESIZE:
            ScreenResizer.full_screen(game_screen)

    @staticmethod
    def resize_screen(game_screen, screen_dimensions):
        m = re.findall('[0-9]+', str(get_monitors()))
        if screen_dimensions[0] == int(m[0]) and screen_dimensions[1] == int(m[1]):
            screen = pygame.display.set_mode((int(m[0]), int(m[1])), FULLSCREEN | HWSURFACE | DOUBLEBUF)
        else:
            screen = pygame.display.set_mode(screen_dimensions, HWSURFACE | DOUBLEBUF)
        game_screen.resize_screen(screen)

    @staticmethod
    def full_screen(game_screen):
        m = re.findall('[0-9]+', str(get_monitors()))
        screen = pygame.display.set_mode((int(m[0]), int(m[1])), FULLSCREEN | HWSURFACE | DOUBLEBUF)
        game_screen.resize_screen(screen)
