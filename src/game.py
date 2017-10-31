"""Main game class."""

import sys

import pygame

from . import assets, settings, utils
from .importation import get_level
from .aiplayer import load_ai
from .bullet_cursor import Cursor
from .levelloop import main as level_main
from .levelselection import level_selection_menu
from .leveleditor import level_editor
from .options import options_menu


class Game:
    """Main game class."""

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        pygame.display.set_caption(settings.GAME_NAME)
        icon = assets.image(settings.WINDOW_ICON_IMAGE)
        pygame.display.set_icon(icon)
        self.sounds = {}
        self.buttons = []
        pygame.mouse.set_visible(False)
        self.cursor = Cursor()
        self.background = utils.Background(-1)
        self.screen.blit(self.background.image, (0, 0))
        self.clock = pygame.time.Clock()
        self.ai_tanks = []
        self.font = assets.font(size=36)
        self.bigfont = assets.font(size=72)
        self.running = False

    def add_button(self, button, on_click=None):
        if on_click is not None:
            button.on_click = on_click
        self.buttons.append(button)
        return button

    def load(self):
        utils.play_default_theme()
        self.sounds['click'] = assets.sound(settings.DEFAULT_CLICK_SOUND)
        walls_group, pits_group, player_pos, ai_pos, _ = get_level(
            settings.BASE_DIR, -1)
        self.walls = walls_group
        self.pits = pits_group

        self.ai_tanks = [load_ai(name, pos, target=player_pos)
                         for name, pos in ai_pos]

        self.title = self.bigfont.render('TANK GAME', color=(30, 30, 30))
        self.titlepos = self.title.get_rect(centerx=512, centery=100)

        self.buttons = []

        # build the buttons

        def start_game():
            self.click()
            pygame.mixer.music.fadeout(200)
            self.clock.tick(5)
            level = 1
            next_level = level_main(level, start=True)
            while next_level:
                level += 1
                next_level = level_main(level)
            if not pygame.mixer.get_init():
                return
            utils.play_default_theme(force=True)
            pygame.display.set_caption(settings.GAME_NAME)

        self.add_button(
            utils.Button("Start Game", self.font, 512, 200, (200, 0, 0)),
            start_game)

        def select_level():
            self.click()
            if not level_selection_menu():
                self.stop()
            else:
                pygame.display.set_caption(settings.GAME_NAME)

        self.add_button(
            utils.Button("Level Selection", self.font, 512, 300, (200, 0, 0)),
            select_level)

        def editor():
            if sys.platform == 'win32':
                self.click()
                self.stop()
                level_editor()

        self.add_button(
            utils.Button("Level Editor", self.font, 512, 400, (200, 0, 0)),
            editor)

        def options():
            self.click()
            if not options_menu():
                return

        self.add_button(
            utils.Button("Options", self.font, 512, 500, (200, 0, 0)),
            options)

        def exit_game():
            self.click()
            self.stop()

        self.add_button(
            utils.Button("Exit Game", self.font, 512, 600, (200, 0, 0)),
            exit_game)

        self.running = True

    def stop(self, clock_delay=5):
        self.running = False
        self.clock.tick(clock_delay)
        pygame.quit()

    def click(self):
        self.sounds['click'].play()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(200)
                self.stop()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.highlighten:
                        button.on_click()

    def update(self):
        self.screen.blit(self.background.image, (0, 0))
        self.screen.blit(self.title, self.titlepos)
        for button in self.buttons:
            button.update()
        self.cursor.update()

        for ai in self.ai_tanks:
            ai.update(settings.BASE_DIR, self.cursor.rect.center,
                      self.walls, self.pits, [], in_menu=True)

        pygame.display.flip()

    def display(self):
        pass

    def run(self):
        self.load()
        while self.running:
            self.clock.tick(60)
            self.update()
            self.events()


def run_game():
    """Main loop."""
    game = Game()
    game.run()
