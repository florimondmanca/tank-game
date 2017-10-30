"""General utility functions."""

# Imports

import pygame
from pygame.locals import *
import math
import os
import sys
from . import settings
join = os.path.join
path = os.getcwd()


def _load_image(filename):
    """Load an image.

    Searches for the image in the IMG_DIRS from the settings.py file.
    If image is not found, raises a FileNotFound exception.

    load_image('img.png') -> pygame.Surface
    """
    for img_dir in settings.IMG_DIRS:
        image_path = os.path.join(settings.BASE_DIR, img_dir, filename)
        try:
            image = pygame.image.load(image_path)
            return image
        except:
            pass
    raise FileNotFoundError(
        '{} does not exist. Directories searched: {}'
        .format(filename, ', '.join(settings.IMG_DIRS)))


def load_image(filename, convert_alpha=None):
    """Load an image.

    Searches for the image in the IMG_DIRS from the settings.py file.
    If image is not found, raises a FileNotFound exception.

    load_image('img.png') -> (pygame.Surface, pygame.Rect)

    Parameters
    ----------
    filename : str
        The image's file name, e.g. 'mysprite.png'.
    convert_alpha : bool
        If False, calls convert() on the image.
        If True, calls convert_alpha().
        Defaults to None: alpha conversion is then derived from the image's
        get_alpha() value: convert_alpha = get_alpha() is not None.
    """
    pygame.display.get_surface()
    image = _load_image(filename)

    if convert_alpha is None:
        convert_alpha = image.get_alpha() is not None
    if convert_alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image, image.get_rect()


def load_sound(filename):
    """Load a sound.

    Searches for the sound in the SOUND_DIRS from the settings.py file.
    If sound is not found, raises a FileNotFound exception.

    Parameters
    ----------
    filename : str
        The sound's file name, e.g. 'click_sound.wav'.
    """
    for sound_dir in settings.SOUND_DIRS:
        sound_path = os.path.join(settings.BASE_DIR, sound_dir, filename)
        try:
            sound = pygame.mixer.Sound(sound_path)
            return sound
        except Exception as e:
            print(e)
            pass
    raise FileNotFoundError(
        '{} does not exist. Directories searched: {}'
        .format(filename, ', '.join(settings.SOUND_DIRS)))


def load_font(*, name=None, size=12):
    # TODO
    pass


def load_image_old(path, name):
    """
    load_image(path, name) -> (Surface, Rect)
    Loads the image 'name' of absolute path 'path', and returns its Surface as well as the associeted Rect object.
    """

    fullname = join(path, name)
    screen = pygame.display.get_surface()
    image = pygame.image.load(fullname)

    if image.get_alpha() is None or name in ['background.png', 'background_menu.png']:
        image = image.convert()
    else:
        image = image.convert_alpha()
    return (image, image.get_rect())


# Miscallenous functions

def update_music_menu():
    """update_music_menu() : if not music is being played, play the MenuTheme"""
    if not pygame.mixer.music.get_busy():  # if no music is being played
        chemin_musique = join(path, "music")
        if sys.platform == "win32":
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
            pygame.mixer.music.load(join(chemin_musique, "MenuTheme.ogg"))
        else:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
            pygame.mixer.music.load(join(chemin_musique, "MenuTheme.wav"))
        pygame.mixer.music.set_volume(get_volumes()[0])
        pygame.mixer.music.play(-1)


def get_volumes():
    with open(join(path, "options.txt"), "r") as options_txt:
        music_volume = float(options_txt.readline())  # when a tank gets shot by a bullet
        fx_volume = float(options_txt.readline())  # when a bullet is fired
    return (music_volume, fx_volume)


def get_size():  # default Tank Game window size
    return (1024, 672)


## A* functions


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
        self.rect = font.render(text, 1, color).get_rect()
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
        text = self.font.render(self.text, 1, color)
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


class SlideButton(Button):
    """SlideButton : a sliding button, heritates from Button.
    Useful in the "options" menu."""

    def __init__(self, text, font, x, y, color):
        Button.__init__(self, text, font, x, y, color)
        self.rect = font.render(text, 1, color).get_rect()
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
        texte = self.font.render(self.text, 1, self.color)
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
            self.image = load_image('background_menu.png')[0]
        else:
            self.image = load_image('background.png')[0]
