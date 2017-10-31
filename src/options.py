"""Options."""


# Imports

import pygame
import sys
import os
from . import loaders
join = os.path.join

# chemin d'accès aux fichiers

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

from src import utils  # noqa: E402
from src.bullet_cursor import Cursor  # noqa: E402


def options_menu():
    """Loop for options menu."""
    pygame.font.init()
    size = utils.get_size()
    screen = pygame.display.set_mode(size)
    clickSound = loaders.sound("click_sound.wav")
    background = utils.Background(-1)
    screen.blit(background.image, (0, 0))
    pygame.mouse.set_visible(False)
    curseur = Cursor()

    clock = pygame.time.Clock()
    var = 1

    font_big = loaders.font(size=36)
    font_medium = loaders.font(size=20)
    font_small = loaders.font(size=14)

    titre = font_big.render("OPTIONS", (30, 30, 30))
    titrepos = titre.get_rect(centerx=512, centery=50)
    back = utils.Button("Back", font_big, 512, 400, (200, 0, 0))
    credits = font_medium.render(
        "Developed by Guillaume Coiffier & Florimond Manca, 2015",
        (30, 30, 30))
    creditspos = credits.get_rect(centerx=512, centery=640)

    mv, fxv = utils.get_volumes().values()
    x1 = 312 + 400 * mv
    x2 = 312 + 400 * fxv
    music_button = utils.SlideButton("Music",
                                     font_medium, x1, 200, (200, 0, 0))
    noise_button = utils.SlideButton("Sound Effects",
                                     font_medium, x2, 300, (200, 0, 0))

    buttons = [music_button, noise_button]
    numbers = []
    zero = font_small.render('0')
    cent = font_small.render('100')
    numbers = [(zero, zero.get_rect(centerx=312, centery=170)),
               (zero, zero.get_rect(centerx=312, centery=270)),
               (cent, cent.get_rect(centerx=712, centery=170)),
               (cent, cent.get_rect(centerx=712, centery=270))]

    # On lance la boucle d'affichage
    while var:
        clock.tick(60)  # on maximise le fps à 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clickSound.play()
                clock.tick(5)
                pygame.mixer.music.fadeout(200)
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back.highlighten:
                    clickSound.play()
                    return True
                else:
                    for b in buttons:
                        if b.highlighten:
                            clickSound.play()
                            b.bind()
                            break
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                volumes = []
                L = 400
                for button in buttons:
                    button.unbind()
                    volume = (button.cursorx - 312) / L
                    volumes.append(volume)
                string = "\n".join(str(volume) for volume in volumes)
                with open(join(path, "options.txt"), mode='w') as options_txt:
                    options_txt.write(string)
                pygame.mixer.music.set_volume(utils.get_volume('music'))

        screen.blit(background.image, (0, 0))
        screen.blit(titre, titrepos)
        back.update()
        for button in buttons:
            button.update()
        screen.blit(credits, creditspos)
        back.update()
        curseur.update()
        for number in numbers:
            screen.blit(number[0], number[1])
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    options_menu()
    pygame.quit()
