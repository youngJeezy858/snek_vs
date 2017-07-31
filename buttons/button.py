from pygame.locals import *
from gameSpriteSheet import *


class Button(GameSpriteSheet):

    ACTIVE = 0
    INACTIVE = 1

    def __init__(self, image, sprite_dimensions, num_sprites, current_sprite=0,
                 dimensions=(-1, -1), position=(-1, -1), pointer=(-1, -1)):
        super(Button, self).__init__(image, sprite_dimensions, num_sprites, dimensions, position, current_sprite)
        self.pointer = pointer
        self.state = self.INACTIVE

    def check_mouse_key_event(self, event):
        mouse_position = pygame.mouse.get_pos()
        self.state = self.INACTIVE
        if self.rect.collidepoint(mouse_position):
            self.animation_state = self.PLAY_UNTIL_END
            if event.type == MOUSEBUTTONDOWN:
                self.state = self.ACTIVE
        elif self.animation_state == self.PLAY_UNTIL_END or self.animation_state == self.PAUSED_AT_END:
            self.animation_state = self.REWIND_UNTIL_START

    def check_controller_event(self, event):
        if event.type == JOYBUTTONDOWN and event.button == 0:
            self.state = self.ACTIVE

    def update(self):
        super(Button, self).update()
