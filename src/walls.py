"""Defining the decorative objects such as walls and pits."""

# Imports

import os
import pygame
from pygame_assets import load
join = os.path.join


class Wall(pygame.sprite.Sprite):
    """A decorative object which nor tanks nor bullets can pass through."""

    bullet_through = False

    def __init__(self, path, name, i, j):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(32 * j, 32 * i, 32, 32)
        self.pos = (j, i)
        self.image = load.image(name)


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
