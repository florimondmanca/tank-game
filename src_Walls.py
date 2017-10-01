# Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Defining the decorative objects such as walls and pits.

## Imports

import pygame
from pygame.locals import *
import math
import os
from src_Utils import load_image
join = os.path.join

def get_size():
    return (1024, 672)


class Wall(pygame.sprite.Sprite):
    """Wall: a decorative object which nor tanks nor bullets can pass through."""
    def __init__(self, path , name , i , j ):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(32*j , 32*i , 32 , 32)
        self.pos = (j,i)
        self.bullet_through = False
        chemin = join(path , join('images','textures'))
        self.image = load_image(chemin,name)[0]


class Pit(Wall):
    """Pit: a decorative object which tanks cannot pass through, but bullets can.
    Inherits from class Wall."""
    def __init__(self, path, name, i, j):
        Wall.__init__(self, path, name, i, j)
        self.bullet_through = True


class Destructible_Wall(Wall):
    """DestructibleWall: a destructible wall-type decorative object. """
    def __init(self, path, name, i, j) :
        Wall.__init__(self, path, name, i, j)
        self.bullet_through = True
        self.destroyed = False
        self.max_shots = 5 # shots needed to destroy the wall
