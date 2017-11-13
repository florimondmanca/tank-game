"""Bullet and Cursor classes."""
# Imports

import math
import pygame
from pygame_assets import load


class Bullet(pygame.sprite.Sprite):
    """Bullet : a moving sprite that goes in a straight line."""

    def __init__(self, x, y, angle):
        super().__init__()
        self.image, self.rect = load.image_with_rect("bullet.png")
        self.x = x
        self.y = y
        self.speed = 2.2
        self.angle = angle

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.rect.centerx = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.rect.centery = y

    def update(self, blit=True):
        move_x = self.speed * math.cos(self.angle)
        move_y = - self.speed * math.sin(self.angle)
        self.x += move_x
        self.y += move_y
        if blit:
            screen = pygame.display.get_surface()
            screen.blit(self.image, self.rect)


class Cursor(pygame.sprite.Sprite):
    """Simple target cursor replacing the usual mouse cursor."""

    def __init__(self):
        super().__init__()
        self.image, self.rect = load.image_with_rect("cursor.png")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)
