"""Defininition of generic asset management utilities."""


import pygame_assets as assets
from . import settings


def get_font(size=32):
    """Return the default font in a certain size."""
    return assets.load.font(settings.DEFAULT_FONT, size=size)


def get_click_sound():
    """Return the click sound."""
    return assets.load.sound(settings.DEFAULT_CLICK_SOUND)


def get_icon():
    """Return the game icon."""
    return assets.load.image(settings.WINDOW_ICON_IMAGE)
