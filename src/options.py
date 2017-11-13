"""Options."""


# Imports

import os
import pygame
from .assets import get_font, get_click_sound
from . import utils
from .bullet_cursor import Cursor

path = os.getcwd()
join = os.path.join


class Options:
    """Context manager for options reading and writing."""

    def __enter__(self, *args, **kwargs):
        self.file = open(join(path, 'options.txt'), mode='w')
        return self

    def save_volumes(self, volumes):
        self.file.write("\n".join(str(volume) for volume in volumes))

    def __exit__(self, *args, **kwargs):
        self.file.close()


class OptionsMenu:
    """Main game class."""

    fps = 60

    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.get_surface()
        self.cursor = Cursor()
        # init object containers
        self.sounds = {}
        self.sounds['click'] = get_click_sound()
        self.buttons = []
        self.labels = []
        # init background
        self.background = utils.Background(-1)
        self.screen.blit(self.background.image, (0, 0))
        # init clock
        self.clock = pygame.time.Clock()
        # init fonts
        self.fonts = {
            'big': get_font(36),
            'medium': get_font(20),
            'small': get_font(14),
        }
        self.running = False

    def exit_with(self, status):
        self.running = False
        self.status = status

    def add_button(self, button, on_click=None, on_release=None):
        if on_click is not None:
            button.on_click = on_click
        if on_release is not None:
            button.on_release = on_release
        self.buttons.append(button)
        return button

    def create_label(self, text, font_size='medium', color=None):
        font = self.fonts.get(font_size)
        if not font:
            raise ValueError('Unknown font size: {}'.format(font_size))
        if color is None:
            color = (30, 30, 30)
        label = font.render(text, 1, color)
        return label

    def add_label(self, text, font_size='medium', color=None, **kwargs):
        label = self.create_label(text, font_size, color)
        rect = label.get_rect(**kwargs)
        self.labels.append((label, rect))

    def load(self):
        utils.play_default_theme()

        self.add_label('OPTIONS', 'big', centerx=512, centery=50)
        self.add_label(
            'Developed by Guillaume Coiffier & Florimond Manca, 2015',
            'medium',
            centerx=512, centery=640)

        mv, fxv = utils.get_volumes().values()
        x1 = 312 + 400 * mv
        x2 = 312 + 400 * fxv

        # build the buttons

        self.buttons = []

        def go_back():
            self.click()
            self.exit_with(True)
        self.add_button(
            utils.Button('Back', self.fonts['big'], 512, 400, (200, 0, 0)),
            go_back)

        def bind(b):
            self.click()
            b.bind()

        def unbind(b):
            L = 400
            b.unbind()
            volume = (b.cursorx - 312) / L
            self.volumes.append(volume)

        music_button = utils.SlideButton('Music', self.fonts['medium'],
                                         x1, 200, (200, 0, 0))
        self.add_button(
            music_button,
            on_click=lambda: bind(music_button),
            on_release=lambda: unbind(music_button))

        fx_button = utils.SlideButton('Sound effects', self.fonts['medium'],
                                      x2, 300, (200, 0, 0))
        self.add_button(
            fx_button,
            on_click=lambda: bind(fx_button),
            on_release=lambda: unbind(fx_button))

        # slide buttons number labels
        self.add_label('0', 'small', centerx=312, centery=170)
        self.add_label('0', 'small', centerx=312, centery=270)
        self.add_label('100', 'small', centerx=712, centery=170)
        self.add_label('100', 'small', centerx=712, centery=270)

    def stop(self, clock_delay=5):
        pygame.mixer.music.fadeout(200)
        self.clock.tick(clock_delay)
        self.exit_with(False)

    def click(self):
        self.sounds['click'].play()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.click()
                self.stop()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.hover:
                        button.on_click()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.volumes = []
                with Options() as options:
                    for button in self.buttons:
                        button.on_release()
                    options.save_volumes(self.volumes)
                pygame.mixer.music.set_volume(utils.get_volume('music'))

    def update(self):
        self.screen.blit(self.background.image, (0, 0))
        for label, rect in self.labels:
            self.screen.blit(label, rect)
        for button in self.buttons:
            button.update()
        self.cursor.update()
        pygame.display.flip()

    def display(self):
        pass

    def run(self):
        self.load()
        self.running = True
        while self.running:
            self.clock.tick(self.fps)
            self.update()
            self.events()
        return self.status


def options_menu():
    """Main loop."""
    options_menu = OptionsMenu()
    return options_menu.run()


if __name__ == '__main__':
    pygame.init()
    options_menu()
    pygame.quit()
