from startMenu import *
from logger import *
from characterSelector import *
from constants.debugging_flags import *


class ChooseCharacterScreen(GameScreen):
    def __init__(self, screen, clock):
        super(ChooseCharacterScreen, self).__init__(screen, clock)
        self.name = "Choose character screen"
        # Bump dat shit
        pygame.mixer.init()
        pygame.mixer.music.load('music/05-character-select.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        self.logger = Logger(self.name, DEBUG_CHOOSE_CHARACTER_SCREEN)
        self.button_grid = ButtonGrid(1, 2)
        self.button_sprites = pygame.sprite.Group()
        self.start_button = StartGameButton((self.screen.get_width() / 2, self.screen.get_height() - 100))
        self.back_button = BackButton((self.screen.get_width() / 2, self.screen.get_height() - 50))
        self.button_grid.add_button(self.start_button, 0, 0)
        self.button_grid.add_button(self.back_button, 0, 1)
        self.button_sprites.add(self.start_button)
        self.button_sprites.add(self.back_button)
        self.flag_start_menu = False
        self.flag_start_game = False
        self.readied_players = []
        self.selectors = []
        for i in range(0, 4):
            if i < 4:
                self.selectors.append(CharacterSelector(i, (200, 100 * (i + 1))))
            else:
                self.selectors.append(CharacterSelector(i, (600, 100 * (i + 1))))

    def check_event(self, event):
        def find_selector(player_id):
            p_selector = None
            for temp_s in self.selectors:
                temp_player = temp_s.get_player()
                if temp_s.is_unallocated() and p_selector is None:
                    self.logger.debug("check_event", "%d, %d" % (player_id, temp_s.selector_id))
                    p_selector = temp_s
                elif temp_s.player_id == player_id:
                    return temp_s
            return p_selector

        if event.type in self.CONTROLLER_EVENTS:
            s = find_selector(event.joy)
            if s.selection_stage == 0 and event.type == JOYBUTTONDOWN and event.button == 2:
                self.back_button.state = Button.ACTIVE
            elif s.get_player() is not None and event.type == JOYBUTTONDOWN and\
                    (event.button == 0 or event.button == 7):
                self.start_button.state = Button.ACTIVE
            else:
                s.check_event(event)
        elif event.type in self.MOUSE_KEY_EVENTS:
            s = find_selector(-1)
            s.check_event(event)
            if s.get_player() is not None:
                self.start_button.check_mouse_key_event(event)
            self.back_button.check_mouse_key_event(event)

    def update(self):
        super(ChooseCharacterScreen, self).update()
        for selector in self.selectors:
            selector.update(self.screen)
        self.button_sprites.update()
        self.button_sprites.draw(self.screen)
        if self.back_button.state == Button.ACTIVE:
            self.needs_switch = True
            self.flag_start_menu = True
        if self.start_button.state == Button.ACTIVE:
            self.needs_switch = True
            self.flag_start_game = True

    def next_screen(self):
        pygame.mixer.music.stop()
        if self.flag_start_menu:
            return startMenu.StartMenu(self.screen, self.clock)
        elif self.flag_start_game:
            players = []
            for selector in self.selectors:
                temp_player = selector.get_player()
                if temp_player is not None:
                    players.append(temp_player)
            return ActiveGame(self.screen, self.clock, players)
