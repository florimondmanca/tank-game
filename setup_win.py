"""Setup file for Windows."""
import os
import sys
chemin = os.getcwd()
if chemin not in sys.path:
    sys.path.append(chemin)

from cx_Freeze import setup, Executable

DATA_FILES = ['images', 'music', 'levels', 'custom_levels', 'fonts']

OPTIONS = {
    'include_files': [
        'images', 'music', 'levels', 'custom_levels', 'unlocked.txt'],
    'compressed': True,
    'path': sys.path + ["Lib"]
}
EXE = [Executable("Tank Game.py", base='Win32GUI')]

setup(
    name="TANK GAME",
    options={"build_exe": OPTIONS},
    executables=EXE
)
