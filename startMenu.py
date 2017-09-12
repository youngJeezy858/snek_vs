from gameScreen import *
from buttons.buttonGrid import *
from buttons.quitGameButton import *
from buttons.startGameButton import *
from buttons.optionsGameButton import *
from buttons.fullscreenGameButton import *
from buttons.backButton import *
from static_classes.screenResizer import *
from activeGame import *
from constants.window_constants import *
from chooseCharacterScreen import *


class StartMenu(GameScreen):

    def __init__(self, screen, clock):
        super(StartMenu, self).__init__(screen, clock)
        self.name = "start menu"
        # Bump dat shit
        pygame.mixer.init()
        pygame.mixer.music.load('music/04-main-menu.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        # Instantiate start menu grid
        self.start_menu_button_grid = ButtonGrid(1, 3)
        # Instantiate start menu sprites
        self.button_start_game = StartGameButton()
        self.button_options = OptionsGameButton()
        button_quit = QuitGameButton()
        self.start_menu_button_grid.add_button(button_quit, 0, 0)
        self.start_menu_button_grid.add_button(self.button_options, 0, 1)
        self.start_menu_button_grid.add_button(self.button_start_game, 0, 2)
        self.start_menu_sprites = pygame.sprite.Group()
        self.start_menu_sprites.add(self.button_start_game)
        self.start_menu_sprites.add(self.button_options)
        self.start_menu_sprites.add(button_quit)
        # Instantiate the options menu sprites
        self.button_fullscreen = FullscreenGameButton()
        self.button_back = BackButton()
        self.options_menu_sprites = pygame.sprite.Group()
        self.options_menu_sprites.add(self.button_fullscreen)
        self.options_menu_sprites.add(self.button_back)
        self.options_menu_button_grid = ButtonGrid(1, 2)
        self.options_menu_button_grid.add_button(self.button_fullscreen, 0, 1)
        self.options_menu_button_grid.add_button(self.button_back, 0, 0)
        # Set the default sprites and other listeners
        self.sprites = self.start_menu_sprites
        self.grid_listener = self.start_menu_button_grid
        # Figure out if the screen needs to be resized
        if self.screen.get_width() != WINDOW_SIZE[0] or self.screen.get_height() != WINDOW_SIZE[1]:
            ScreenResizer.resize_screen(self, (self.screen.get_width(), self.screen.get_height()))

    def check_event(self, event):
        if self.is_controller_active(event):
            self.grid_listener.check_controller_event(event)
        else:
            self.grid_listener.check_mouse_key_event(event)

    def update(self):
        super(StartMenu, self).update()
        self.sprites.update()
        self.sprites.draw(self.screen)
        # Check the screen/spritegroup switchers
        if self.button_start_game.state == Button.ACTIVE:
            self.button_start_game.state = Button.INACTIVE
            self.needs_switch = True
        if self.button_options.state == Button.ACTIVE:
            self.button_options.state = Button.INACTIVE
            self.sprites = self.options_menu_sprites
            self.grid_listener = self.options_menu_button_grid
        if self.button_back.state == Button.ACTIVE:
            self.button_back.state = Button.INACTIVE
            self.sprites = self.start_menu_sprites
            self.grid_listener = self.start_menu_button_grid
        if self.button_fullscreen.state == Button.ACTIVE:
            self.button_fullscreen.flip_screen_mode(self)

    def next_screen(self):
        pygame.mixer.music.stop()
        return ChooseCharacterScreen(self.screen, self.clock)

    def resize_screen(self, screen):
        super(StartMenu, self).resize_screen(screen)
        for sprite in self.options_menu_sprites:
            dimensions = self.calculate_dimensions(sprite.og_dimensions)
            position = self.calculate_position(sprite.og_position)
            sprite.resize(dimensions, position)
        for sprite in self.start_menu_sprites:
            dimensions = self.calculate_dimensions(sprite.og_dimensions)
            position = self.calculate_position(sprite.og_position)
            sprite.resize(dimensions, position)
