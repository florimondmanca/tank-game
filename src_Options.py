# Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Options


# Imports

import pygame
from pygame.locals import *
from pygame.font import *
import math
import sys
import os
join = os.path.join

# chemin d'accès aux fichiers

path = os.getcwd()
if path not in sys.path:
    sys.path.append(path)

import src_Utils as Utils
from src.bullet_cursor import Cursor


def options_menu():
    pygame.font.init()
    size = Utils.get_size()
    screen = pygame.display.set_mode(size)
    clickSound = pygame.mixer.Sound(join(join(path, "music"), "click_sound.wav"))
    background = Utils.Background(join(path, "images"), -1)
    screen.blit(background.image, (0, 0))
    pygame.mouse.set_visible(False)
    curseur = Cursor(join(path, "images"))

    clock = pygame.time.Clock()
    var = 1

    font1 = pygame.font.Font(join(path, join("fonts", "BOMBARD.ttf")), 36)
    font2 = pygame.font.Font(join(path, join("fonts", "BOMBARD.ttf")), 20)
    font3 = pygame.font.Font(join(path, join("fonts", "BOMBARD.ttf")), 14)

    titre = font1.render("OPTIONS", 1, (30, 30, 30))
    titrepos = titre.get_rect(centerx=512, centery=50)
    back = Utils.Button("Back", font1, 512, 400, (200, 0, 0))
    credits = font2.render("Developped by Guillaume Coiffier & Florimond Manca, 2015",
                           1, (30, 30, 30))
    creditspos = credits.get_rect(centerx=512, centery=640)

    mv, fxv = Utils.get_volumes()
    x1 = 312 + 400 * mv
    x2 = 312 + 400 * fxv
    music_button = Utils.SlideButton("Music", font2, x1, 200, (200, 0, 0))
    noise_button = Utils.SlideButton("Sound Effects", font2, x2, 300, (200, 0, 0))

    buttons = [music_button, noise_button]
    numbers = []
    zero = font3.render("0", 1, (0, 0, 0))
    cent = font3.render("100", 1, (0, 0, 0))
    numbers = [(zero, zero.get_rect(centerx=312, centery=170)),
               (zero, zero.get_rect(centerx=312, centery=270)),
               (cent, cent.get_rect(centerx=712, centery=170)),
               (cent, cent.get_rect(centerx=712, centery=270))]

    # On lance la boucle d'affichage
    while var:
        clock.tick(60)  # on maximise le fps à 60
        for event in pygame.event.get():
            if event.type == QUIT:
                clickSound.play()
                clock.tick(5)
                pygame.mixer.music.fadeout(200)
                pygame.quit()
                return False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if back.highlighten:
                    clickSound.play()
                    return True
                else:
                    for b in buttons:
                        if b.highlighten:
                            clickSound.play()
                            b.bind()
                            break
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                volumes = []
                L = 400
                for button in buttons:
                    button.unbind()
                    volume = (button.cursorx - 312) / L
                    volumes.append(volume)
                string = "\n".join(str(volume) for volume in volumes)
                with open(join(path, "options.txt"), mode='w') as options_txt:
                    options_txt.write(string)
                pygame.mixer.music.set_volume(Utils.get_volumes()[0])

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
