"""
Tank Game: A game with tanks and stuff.

by Erkalys & Florimond Manca

Defining the decorative objects such as walls and pits.
"""

# Imports

import pygame
import os
from src_Utils import load_image
join = os.path.join


def get_size():
    return (1024, 672)


class Wall(pygame.sprite.Sprite):
    """A decorative object which nor tanks nor bullets can pass through."""

    bullet_through = False

    def __init__(self, path, name, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(32 * j, 32 * i, 32, 32)
        self.pos = (j, i)
        chemin = join(path, join('images', 'textures'))
        self.image = load_image(chemin, name)[0]


class Pit(Wall):
    """A decorative object which tanks cannot pass through, but bullets can."""

    bullet_through = True


class DestructibleWall(Wall):
    """DestructibleWall: a destructible wall-type decorative object."""

    bullet_through = True

    def __init(self, path, name, i, j):
        Wall.__init__(self, path, name, i, j)
        self.destroyed = False
        self.max_shots = 5  # shots needed to destroy the wall
