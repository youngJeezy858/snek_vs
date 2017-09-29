from gameSprite import *


class GameSpriteSheet(GameSprite):

    # Constants for animation states
    PAUSED_AT_START = '0'
    PAUSED_AT_END = '1'
    PLAY_UNTIL_END = '2'
    PLAY_ENDLESSLY = '3'
    PLAY_AND_RESET = '4'
    REWIND_UNTIL_START = '5'
    REWIND_ENDLESSLY = '6'

    def __init__(self, image, sprite_dimensions, num_sprites, dimensions, position, current_sprite=0):
        super(GameSpriteSheet, self).__init__(image, dimensions, position)
        self.sprite_dimensions = sprite_dimensions
        self.num_sprites = num_sprites
        self.current_sprite = current_sprite
        self.animation_state = self.PAUSED_AT_START
        self.sprite_sheet_master = pygame.image.load(image)
        self.set_image(self.current_sprite)

    def set_image(self, sprite_position):
        if sprite_position >= self.num_sprites:
            raise ValueError('sprite_position must not exceed number of sprites in the sprite sheet')
        x = self.sprite_dimensions[0] * sprite_position
        y = 0
        x_offset = self.sprite_dimensions[0]
        y_offset = self.sprite_dimensions[1]
        rect = pygame.Rect(x, y, x_offset, y_offset)
        self.image_master = pygame.Surface(rect.size)
        self.image_master.blit(self.sprite_sheet_master, (0, 0), rect)
        self.image_master = self.image_master
        self.image_master = pygame.transform.smoothscale(self.image_master, self.dimensions)
        self.image = self.image_master
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    @abstractmethod
    def check_event(self, event):
        return 1

    @abstractmethod
    def update(self):
        if self.animation_state == self.PLAY_UNTIL_END:
            if self.current_sprite + 1 == self.num_sprites:
                self.animation_state = self.PAUSED_AT_END
            else:
                self.current_sprite += 1

        elif self.animation_state == self.PLAY_AND_RESET:
            if self.current_sprite + 1 == self.num_sprites:
                self.animation_state = self.PAUSED_AT_START
                self.current_sprite = 0
            else:
                self.current_sprite += 1

        elif self.animation_state == self.PLAY_ENDLESSLY:
            if self.current_sprite + 1 == self.num_sprites:
                self.current_sprite = 0
            else:
                self.current_sprite += 1

        elif self.animation_state == self.REWIND_UNTIL_START:
            if self.current_sprite == 0:
                self.animation_state = self.PAUSED_AT_START
            else:
                self.current_sprite -= 1

        elif self.animation_state == self.REWIND_ENDLESSLY:
            if self.current_sprite == 0:
                self.current_sprite = self.num_sprites - 1
            else:
                self.current_sprite -= 1

        self.set_image(self.current_sprite)

 #   @abstractmethod
#    def resize(self, dimensions, position):
#        return 1