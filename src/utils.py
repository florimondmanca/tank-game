"""General utility functions."""

# Imports

import pygame
from pygame.locals import *
import os
import sys

from . import assets, settings

join = os.path.join
path = os.getcwd()


# Miscallenous functions

def get_default_theme(platform=sys.platform):
    """Get default theme for given platform."""
    if platform == 'win32':
        return settings.DEFAULT_THEME_WIN
    else:
        return settings.DEFAULT_THEME


def play_default_theme(force=False):
    """If no music is being played, play the default theme."""
    if force or not pygame.mixer.music.get_busy():
        v = get_volume('music')
        theme = get_default_theme()
        assets.music(theme, volume=v)
        pygame.mixer.music.play(-1)


def update_music_menu():
    """If no music is being played, play the menu theme."""
    if not pygame.mixer.music.get_busy():  # if no music is being played
        v = get_volume('music')
        if sys.platform == "win32":
            assets.music('MenuTheme.ogg', volume=v)
        else:
            assets.music('MenuTheme.wav', volume=v)
        pygame.mixer.music.play(-1)


def get_volumes():
    """Get the volumes from the options.

    Return a dictionnary mapping the volume parameters to their value.
    """
    with open(join(path, "options.txt"), "r") as options_txt:
        music_volume = float(options_txt.readline())
        fx_volume = float(options_txt.readline())
    return {
        'music': music_volume,
        'fx': fx_volume
    }


def get_volume(parameter):
    """Get the volume for a single parameter.

    Parameters
    ----------
    parameter : str
        Name of the volume parameter.
    """
    volumes = get_volumes()
    return volumes[parameter]


def get_size():  # default Tank Game window size
    return (1024, 672)


# A* functions


def heuristic(a, b):
    '''
    The heuristic function of the A*
    '''
    x = b[0] - a[0]
    y = b[1] - a[1]
    return (x * x + y * y)


def get_neighbors(obstacles, x):
    '''
    Returns the list of each cell which is adjacent to the (i, j) cell
    '''
    i, j = x
    neighbors = []
    if j > 0 and obstacles[i, j - 1]:
        neighbors.append((i, j - 1))
    if j < 20 and obstacles[i, j + 1]:
        neighbors.append((i, j + 1))
    if i > 0 and obstacles[i - 1, j]:
        neighbors.append((i - 1, j))
    if i < 31 and obstacles[i + 1, j]:
        neighbors.append((i + 1, j))
    return neighbors


def clean(a_list):
    '''
    Removes the unnecessary (x, y) points of a list
    Only points that forms a corner of the path are necessary
    '''
    new_list = [x for x in a_list]
    popped = 0
    for i in range(1, len(a_list) - 1):
        (xi, yi) = a_list[i]
        (xsuiv, ysuiv) = a_list[i + 1]
        (xprec, yprec) = a_list[i - 1]
        if (xi == xsuiv and xi == xprec) or (yi == ysuiv and yi == yprec):  # remove the middle point if 3 points are aligned
            new_list.pop(i - popped)
            popped += 1
    return new_list


# Utility Classes

class Button:
    """Button: a standard clickable button. Automatized highlighting.
    """

    def __init__(self, text, font, x, y, color):
        self.text = text  # string
        self.font = font  # SysFont object
        self.rect = font.render(text, color).get_rect()
        self.rect.center = (x, y)
        self.highlighten = False
        self.color = color  # RGB: (r, g, b)

    def update(self):
        screen = pygame.display.get_surface()
        x, y = pygame.mouse.get_pos()
        if not self.highlighten:
            if self.rect.collidepoint(x, y):
                self.highlighten = True
        else:
            if not self.rect.collidepoint(x, y):
                self.highlighten = False
        color = self.highlight()
        text = self.font.render(self.text, color)
        screen.blit(text, self.rect)

    def highlight(self):
        """highlight(): met le bouton en évidence
        """
        (r, g, b) = self.color
        if self.highlighten:
            r = min(r + 70, 255)
            b = min(b + 70, 255)
            g = min(g + 70, 255)
        return (r, g, b)

    def on_click(self):
        pass


class SlideButton(Button):
    """SlideButton : a sliding button, heritates from Button.
    Useful in the "options" menu."""

    def __init__(self, text, font, x, y, color):
        Button.__init__(self, text, font, x, y, color)
        self.rect = font.render(text, color).get_rect()
        self.rect.bottom += 50
        self.rect.centerx, self.rect.top = get_size()[0] // 2, y
        self.cursorx = x
        self.cursorrect = pygame.rect.Rect(x - 3, self.rect.bottom - 50, 6, 20)
        self.textrect = pygame.rect.Rect(self.rect.left, self.rect.top - 50,
                                         self.rect.height - 50, self.rect.width)
        self.bound = False

    def update(self):
        x0 = get_size()[0] // 2
        screen = pygame.display.get_surface()
        y0 = self.rect.bottom - 40
        line = pygame.draw.line(screen, (0, 0, 0), (x0 - 200, y0), (x0 + 200, y0))
        x, y = pygame.mouse.get_pos()
        if not self.highlighten:
            if self.cursorrect.collidepoint(x, y):
                self.highlighten = True
        else:
            if not self.cursorrect.collidepoint(x, y):
                self.highlighten = False
        color = self.highlight()
        texte = self.font.render(self.text, self.color)
        screen.blit(texte, self.textrect)
        if self.bound and abs(x0 - x) <= 200:
            self.cursorrect.centerx = x
            self.cursorx = x
        pygame.draw.rect(screen, color, self.cursorrect)

    def bind(self):
        """Bind the slider to the mouse."""
        self.bound = True

    def unbind(self):
        """Unbind the slider to the mouse."""
        self.bound = False


class Background:

    def __init__(self, nlevel=-1, custom=False):
        # nlevel : the identifier of the loaded level. -1 for menus.
        if nlevel == -1 or (nlevel >= 20 and not custom):
            self.image = assets.image('background_menu.png')
        else:
            self.image = assets.image('background.png')
