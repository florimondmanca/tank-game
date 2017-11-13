"""Bullet and Cursor classes."""
# Imports

import os
import math
import pygame
from pygame_assets import load

path = os.getcwd()


# Classes Boulet, Curseur

class Bullet(pygame.sprite.Sprite):
    """Bullet : a moving sprite that goes in a straight line."""

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image_with_rect("bullet.png")
        self.rect.centerx = x
        self.rect.centery = y
        self.true_pos = (x, y)  # (float, float)
        self.speed = 2.2  # bullet's speed
        self.angle = angle  # trajectory angle with the x axis

    def update(self, blit=True):
        move_x = self.speed * math.cos(self.angle)
        move_y = - self.speed * math.sin(self.angle)
        new_x = self.true_pos[0] + move_x
        new_y = self.true_pos[1] + move_y
        self.true_pos = (new_x, new_y)
        self.rect.center = (int(new_x), int(new_y))
        if blit:
            screen = pygame.display.get_surface()
            screen.blit(self.image, self.rect)


class Cursor(pygame.sprite.Sprite):
    """Simple cursor replacing the usual mouse cursor."""

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load.image_with_rect("cursor.png")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)
