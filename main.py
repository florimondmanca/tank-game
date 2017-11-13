"""Main entry point."""
import pygame
import pygame_assets as assets
from src.game import run_game

pygame.init()

assets.config.dirs['image'] += ['background', 'texture']


if __name__ == '__main__':
    run_game()
