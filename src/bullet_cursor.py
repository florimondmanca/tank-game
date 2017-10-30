"""Bullet and Cursor classes."""
# Imports

import pygame
import math
import os
from src import utils

path = os.getcwd()


# Classes Boulet, Curseur

class Bullet(pygame.sprite.Sprite):
    """Bullet : a moving sprite that goes in a straight line."""

    def __init__(self, path, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(path, "bullet.png")
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

    def __init__(self, path):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(path, "cursor.png")

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)
