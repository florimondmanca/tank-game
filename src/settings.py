"""Base settings."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GAME_NAME = "Tank Game"

WINDOW_ICON_IMAGE = 'tank.png'
WINDOW_SIZE = (1024, 672)

IMG_DIRS = [
    "images",
    "images/textures",
    "images/backgrounds",
]
SOUND_DIRS = ['music', 'sounds']
MUSIC_DIRS = ['music']
FONT_DIRS = ['fonts']

DEFAULT_TANK_BODY_IMAGE = "tank_corps_regular.png"
DEFAULT_TANK_CANON_IMAGE = "canon_regular.png"
DEFAULT_TANK_FIRE_SOUND = "shot_sound.wav"

DEFAULT_CLICK_SOUND = 'click_sound.wav'
DEFAULT_THEME = 'MenuTheme.wav'
DEFAULT_THEME_WIN = 'MenuTheme.ogg'

DEFAULT_FONT = 'BOMBARD.ttf'
