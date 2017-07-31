import pygame
from pygame.locals import *
import sys


class ExitListener(object):
    @staticmethod
    def check_event(event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
