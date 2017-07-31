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


class StartMenu(GameScreen):

    def __init__(self, screen, players=[], winner=[]):
        super(StartMenu, self).__init__(screen)
        self.name = "start menu"
        # Instantiate start menu grid
        start_menu_button_grid = ButtonGrid(1, 3)
        # Instantiate start menu sprites
        self.button_start_game = StartGameButton()
        self.button_options = OptionsGameButton()
        button_quit = QuitGameButton()
        start_menu_button_grid.add_button(button_quit, 0, 0)
        start_menu_button_grid.add_button(self.button_options, 0, 1)
        start_menu_button_grid.add_button(self.button_start_game, 0, 2)
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
        # Set the default sprites
        self.sprites = self.start_menu_sprites
        # Instantiate shit from previous game
        self.players = players
        self.winner = winner
        # Figure out if the screen needs to be resized
        if self.screen.get_width() != WINDOW_SIZE[0] or self.screen.get_height() != WINDOW_SIZE[1]:
            print "shit"
            ScreenResizer.resize_screen(self, (self.screen.get_width(), self.screen.get_height()))

    def check_event(self, event):
        for sprite in self.sprites:
            if self.is_controller_active(event):
                sprite.check_controller_event(event)
            else:
                sprite.check_mouse_key_event(event)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.sprites.update()
        self.sprites.draw(self.screen)
        for player in self.players:
            # Draw yo stats foo'
            stats_x = (self.screen.get_width() / (len(self.players) + 1)) * (player.controller_id + 1)
            stats_y = 200
            self.screen.blit(player.stats, (stats_x, stats_y))
        for winner in self.winner:
            winner_x = (self.screen.get_width() / (len(self.winner) + 1)) * (winner.controller_id + 1)
            winner_y = 100
            self.screen.blit(winner.winner_display, (winner_x, winner_y))
        # Check the screen/spritegroup switchers
        if self.button_start_game.needs_switch:
            self.needs_switch = True
        if self.button_options.state == Button.ACTIVE:
            self.button_options.state = Button.INACTIVE
            self.sprites = self.options_menu_sprites
        if self.button_back.state == Button.ACTIVE:
            self.button_back.state = Button.INACTIVE
            self.sprites = self.start_menu_sprites
        if self.button_fullscreen.state == Button.ACTIVE:
            self.button_fullscreen.flip_screen_mode(self)

    def next_screen(self):
        return ActiveGame(self.screen, 1) #dlen(self.controllers))

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
