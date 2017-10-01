# Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Menu loop


# Imports

import pygame
from pygame.locals import *
from pygame.font import *
import math
import sys
import os
join = os.path.join

if sys.platform == "win32":  # si sous windows,
    # on a besoin de ce module pour le standalone
    import pygame._view

# chemin d'accès aux fichiers

MAIN_PATH = os.getcwd()
if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

import src_Tank as Tank_class
import src_Utils as Utils
from src.bullet_cursor import Cursor
from src_AI_Player import *
from src_Walls import *
from src_Level_Loop import main
from src_Importation import get_level
from src_Level_Selection import level_selection_menu
from src_Options import *
import src_Level_Editor as Level_Editor


def run_game():
    pygame.init()
    Utils.update_music_menu()
    clickSound = pygame.mixer.Sound(join(join(MAIN_PATH, "music"), "click_sound.wav"))
    pygame.font.init()  # module de pygame qui gère le texte

    size = Utils.get_size()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tank Game")
    walls_group, pits_group, pos_joueur, pos_IA, blah = get_level(MAIN_PATH, -1)
    icone = pygame.image.load(join(join(MAIN_PATH, 'images'), 'tank.png'))
    pygame.display.set_icon(icone)

    # get the AI data
    AI_group = []
    for element in pos_IA:
        if element[0] == 'yellow':
            yellow = YellowAI(join(MAIN_PATH, "images"),
                              'tank_corps_yellow.png',
                              'canon_yellow.png', element[1],
                              pos_joueur)
            AI_group.append(yellow)
        if element[0] == 'yellowPlus':
            yellowp = YellowPlusAI(join(MAIN_PATH, "images"),
                                   'tank_corps_yellowPlus.png',
                                   'canon_yellowPlus.png',
                                   element[1], pos_joueur)
            AI_group.append(yellowp)
        elif element[0] == 'blue':
            blue = BlueAI(join(MAIN_PATH, "images"),
                          'tank_corps_blue.png',
                          'canon_blue.png',
                          element[1], pos_joueur, [])
            AI_group.append(blue)
        elif element[0] == 'bluePlus':
            bluep = BluePlusAI(join(MAIN_PATH, "images"),
                               'tank_corps_blue.png',
                               'canon_bluePlus.png',
                               element[1], pos_joueur, [])
            AI_group.append(bluep)
        elif element[0] == 'red':
            red = RedAI(join(MAIN_PATH, "images"),
                        'tank_corps_red.png',
                        'canon_red.png',
                        element[1], pos_joueur)
            AI_group.append(red)
        elif element[0] == 'redPlus':
            redp = RedPlusAI(join(MAIN_PATH, "images"),
                             'tank_corps_red.png',
                             'canon_redPlus.png',
                             element[1], pos_joueur)
            AI_group.append(redp)
        elif element[0] == 'purple':
            purple = PurpleAI(join(MAIN_PATH, "images"),
                              'tank_corps_purple.png',
                              'canon_purple.png',
                              element[1], pos_joueur, [])
            AI_group.append(purple)
        elif element[0] == 'purplePlus':
            purplep = PurplePlusAI(join(MAIN_PATH, "images"),
                                   'tank_corps_purple.png',
                                   'canon_purplePlus.png',
                                   element[1], pos_joueur, [])
            AI_group.append(purplep)

    background = Utils.Background(join(MAIN_PATH, "images"), -1)
    screen.blit(background.image, (0, 0))

    pygame.mouse.set_visible(False)
    curseur = Cursor(join(MAIN_PATH, "images"))

    clock = pygame.time.Clock()
    running = 1

    font = pygame.font.Font(join(path, join("fonts", "BOMBARD.ttf")), 36)
    bigfont = pygame.font.Font(join(path, join("fonts", "BOMBARD.ttf")), 72)

    title = bigfont.render("TANK GAME", 1, (30, 30, 30))
    titlepos = title.get_rect(centerx=512, centery=100)

    start_game = Utils.Button("Start Game", font, 512, 200, (200, 0, 0))
    level_select = Utils.Button("Level Selection", font, 512, 300, (200, 0, 0))
    exit_game = Utils.Button("Exit Game", font, 512, 600, (200, 0, 0))
    editor = Utils.Button("Level Editor",  font, 512, 400, (200, 0, 0))
    options = Utils.Button("Options", font, 512, 500, (200, 0, 0))

    while running:
        clock.tick(60)  # on maximise le fps à 60
        screen.blit(background.image, (0, 0))
        screen.blit(title, titlepos)
        start_game.update()
        exit_game.update()
        editor.update()
        level_select.update()
        curseur.update()
        options.update()
        Utils.update_music_menu()

        for AI_sprite in AI_group:
            boulets = AI_sprite.update(MAIN_PATH, curseur.rect.center,
                                       walls_group, pits_group, [], in_menu=True)

        pygame.display.flip()

        for event in pygame.event.get():
            # if player wants to quit (using window buttons)
            if event.type == QUIT:
                running = 0
                pygame.mixer.music.fadeout(200)
                clock.tick(5)
                pygame.quit()

            # player clicked somewhere
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                # player clicked on "Exit Game"
                if exit_game.highlighten:
                    running = 0
                    clickSound.play()
                    clock.tick(4)
                    pygame.quit()

                # player clicked on "Start Game"
                elif start_game.highlighten:
                    clickSound.play()
                    pygame.mixer.music.fadeout(200)
                    clock.tick(5)
                    n = 1
                    result = main(n, start=True)
                    while result:
                        n += 1
                        result = main(n)
                    if not pygame.mixer.get_init():
                        return
                    pygame.display.set_caption("Tank Game")

                # player clicked on "Level Selection"
                elif level_select.highlighten:
                    clickSound.play()
                    if not level_selection_menu():
                        running = 0
                        pygame.quit()
                    else:
                        pygame.display.set_caption("Tank Game")

                # player clicked on "Level Editor"
                elif editor.highlighten and sys.platform == "wind32":
                    clickSound.play()
                    running = 0
                    pygame.quit()
                    Level_Editor.level_editor()

                # player clicked on "Options"
                elif options.highlighten:
                    clickSound.play()
                    if not options_menu():
                        return

if __name__ == "__main__":
    run_game()
