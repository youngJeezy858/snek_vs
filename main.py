import os
from constants.window_constants import *
from constants.debugging_flags import *
from startMenu import *
from static_classes.exitListener import *
import unittest


pygame.init()
if RUN_TEST_SUITE:
    test_suite = unittest.TestLoader().discover('.', '*_test.py')
    unittest.TextTestRunner(verbosity=2).run(test_suite)

os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), HWSURFACE | DOUBLEBUF)
pygame.display.set_caption('Snek VS')
clock = pygame.time.Clock()
game_screen = StartMenu(screen, clock)

while True:

    clock.tick(60)
    # The Controller
    for event in pygame.event.get():
        # Static listeners first!
        ExitListener.check_event(event)
        # Check all game objects
        game_screen.check_event(event)

    # The View
    #  The bits that need to alter variables in the main loop
    if game_screen.needs_resize:
        screen = game_screen.resize_screen()
    if game_screen.needs_switch:
        game_screen = game_screen.next_screen()
    #  The bits that update and draw everything else
    game_screen.update()
    pygame.display.update()
