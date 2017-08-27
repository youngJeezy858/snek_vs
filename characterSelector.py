from gameSprite import *
from pygame.locals import *
from constants.player_constants import *
from player import *


class CharacterSelector(object):

    SELCTION_STAGES = [
        'Press start or return',
        'Choose team',
        'Choose color',
        'READY'
    ]

    def __init__(self, selector_id, position):
        self.selector_id = selector_id
        self.team_id = selector_id
        self.shade_id = 1
        self.position = position
        self.player_id = -1000
        self.is_ready = False
        # Define sprites
        self.color = TEAM_COLORS[self.team_id]
        self.sprite_player = GameSprite('images/player_' + self.color + '_1.png', (25, 25), position)
        self.sprite_left_arrow = GameSprite('images/arrow_left.png', (15, 15), (position[0] - 50, position[1]))
        self.sprite_right_arrow = GameSprite('images/arrow_right.png', (15, 15), (position[0] + 50, position[1]))
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.sprite_left_arrow)
        self.sprites.add(self.sprite_right_arrow)
        self.sprites.add(self.sprite_player)
        # Define game states
        self.selection_stage = 0
        # Define fonts
        self.prompt_font = pygame.font.SysFont("monospace", 24)
        self.player_prompt = self.prompt_font.render\
            (self.SELCTION_STAGES[self.selection_stage], True, (255, 255, 255))
        self.player_prompt_rect = self.player_prompt.get_rect(center=(self.position[0], self.position[1] + 30))

    def check_event(self, event):
        if event.type == KEYDOWN:
            if self.player_id == -1000 or self.player_id == -1:
                if event.key == K_RETURN and self.selection_stage < len(self.SELCTION_STAGES) - 1:
                    self.player_id = -1
                    self.selection_stage += 1
                elif event.key == K_ESCAPE:
                    if self.player_id != -1000:
                        self.selection_stage -= 1
                        if self.selection_stage == 0:
                            self.player_id = -1000
        elif event.type == JOYBUTTONDOWN:
            if self.player_id == -1000 or self.player_id == event.joy:
                if (event.button == 7 or event.button == 0) and self.selection_stage < len(self.SELCTION_STAGES) - 1:
                    self.player_id = event.joy
                    self.selection_stage += 1
                elif event.button == 1:
                    if self.player_id != -1000:
                        self.selection_stage -= 1
                        if self.selection_stage == 0:
                            self.player_id = -1000
        elif event.type == MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if self.sprite_left_arrow.rect.collidepoint(mouse_position):
                if self.selection_stage == 1:
                    self.update_team_id(1)
                elif self.selection_stage == 2:
                    self.update_shade_id(1)
            elif self.sprite_right_arrow.rect.collidepoint(mouse_position):
                if self.selection_stage == 1:
                    self.update_team_id(-1)
                elif self.selection_stage == 2:
                    self.update_shade_id(-1)
        elif event.type == JOYHATMOTION and self.player_id == event.joy:
            if self.selection_stage == 1:
                self.update_team_id(event.value[0])
            elif self.selection_stage == 2:
                self.update_shade_id(event.value[0])

    def update_team_id(self, i):
        self.team_id += i
        if self.team_id > len(self.SELCTION_STAGES) - 1:
            self.team_id = 0
        elif self.team_id < 0:
            self.team_id = len(self.SELCTION_STAGES) - 1
        self.sprites.remove(self.sprite_player)
        self.color = TEAM_COLORS[self.team_id]
        self.shade_id = 1
        self.sprite_player = GameSprite('images/player_' + self.color + '_' + str(self.shade_id) + '.png',
                                        (25, 25), self.position)
        self.sprites.add(self.sprite_player)

    def update_shade_id(self, i):
        self.shade_id += i
        if self.shade_id > NUM_SHADES:
            self.shade_id = 1
        elif self.shade_id < 1:
            self.shade_id = NUM_SHADES - 1
        self.sprites.remove(self.sprite_player)
        self.sprite_player = GameSprite('images/player_' + self.color + '_' + str(self.shade_id) + '.png',
                                        (25, 25), self.position)
        self.sprites.add(self.sprite_player)

    def update(self, screen):
        self.player_prompt_rect = self.player_prompt.get_rect(center=(self.position[0], self.position[1] + 30))
        self.player_prompt = self.prompt_font.render\
                            (self.SELCTION_STAGES[self.selection_stage], True, (255, 255, 255))
        screen.blit(self.player_prompt, self.player_prompt_rect)
        if self.selection_stage != 0:
            self.sprites.draw(screen)

    def get_player(self):
        if self.selection_stage == len(self.SELCTION_STAGES) - 1:
            return Player(self.color, self.shade_id, (25, 25), (100, 100 * (self.selector_id+1)), self.player_id, 3)
        else:
            return None

    def is_unallocated(self):
        if self.player_id == -1000:
            return True
        else:
            return False
