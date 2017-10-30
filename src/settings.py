"""Base settings."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMG_DIRS = [
    "images",
    "images/textures",
    "images/backgrounds",
]
SOUND_DIRS = ['music', 'sounds']
MUSIC_DIRS = ['music']

DEFAULT_TANK_BODY_IMAGE = "tank_corps_regular.png"
DEFAULT_TANK_CANON_IMAGE = "canon_regular.png"
DEFAULT_TANK_FIRE_SOUND = "shot_sound.wav"
