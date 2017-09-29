from abc import *
import pygame


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.og_dimensions = dimensions
        self.og_position = position
        self.dimensions = dimensions
        self.position = position
        self.image_path = image
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, dimensions)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def resize(self, dimensions, position):
        self.dimensions = dimensions
        self.image = pygame.transform.smoothscale(self.image_master, dimensions)
        self.mask = pygame.mask.from_surface(self.image)
        self.image = self.image_master
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position

    @abstractmethod
    def check_event(self, event):
        return

    @abstractmethod
    def update(self):
        self.rect.center = self.position
