"""Main menu loop."""


# Imports

import pygame
import sys
import os
from . import loaders
from . import utils
from . import settings
from .bullet_cursor import Cursor
from .aiplayer import YellowAI, YellowPlusAI, BlueAI, BluePlusAI, RedAI, \
    RedPlusAI, PurpleAI, PurplePlusAI
from .levelloop import main
from .importation import get_level
from .levelselection import level_selection_menu
from .options import options_menu
import src.leveleditor as Level_Editor

# if sys.platform == "win32":
#     import pygame._view

join = os.path.join
MAIN_PATH = os.getcwd()


def run_game():
    """Main game loop."""
    pygame.init()
    utils.update_music_menu()
    clickSound = loaders.sound(settings.DEFAULT_CLICK_SOUND)
    pygame.font.init()  # module de pygame qui gère le texte

    size = utils.get_size()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(settings.GAME_NAME)
    walls_group, pits_group, pos_joueur, pos_IA, blah = get_level(
        MAIN_PATH, -1)
    icon = loaders.image(settings.WINDOW_ICON_IMAGE)
    pygame.display.set_icon(icon)

    # get the AI data
    AI_group = []
    for element in pos_IA:
        if element[0] == 'yellow':
            yellow = YellowAI(element[1],
                              pos_joueur)
            AI_group.append(yellow)
        if element[0] == 'yellowPlus':
            yellowp = YellowPlusAI(element[1], pos_joueur)
            AI_group.append(yellowp)
        elif element[0] == 'blue':
            blue = BlueAI(element[1], pos_joueur, [])
            AI_group.append(blue)
        elif element[0] == 'bluePlus':
            bluep = BluePlusAI(element[1], pos_joueur, [])
            AI_group.append(bluep)
        elif element[0] == 'red':
            red = RedAI(element[1], pos_joueur)
            AI_group.append(red)
        elif element[0] == 'redPlus':
            redp = RedPlusAI(element[1], pos_joueur)
            AI_group.append(redp)
        elif element[0] == 'purple':
            purple = PurpleAI(element[1], pos_joueur, [])
            AI_group.append(purple)
        elif element[0] == 'purplePlus':
            purplep = PurplePlusAI(element[1], pos_joueur, [])
            AI_group.append(purplep)

    background = utils.Background(-1)
    screen.blit(background.image, (0, 0))

    pygame.mouse.set_visible(False)
    curseur = Cursor()

    clock = pygame.time.Clock()
    running = 1

    font = loaders.font(size=36)
    bigfont = loaders.font(size=72)

    title = bigfont.render('TANK GAME', color=(30, 30, 30))
    titlepos = title.get_rect(centerx=512, centery=100)

    start_game = utils.Button("Start Game", font, 512, 200, (200, 0, 0))
    level_select = utils.Button("Level Selection", font, 512, 300, (200, 0, 0))
    exit_game = utils.Button("Exit Game", font, 512, 600, (200, 0, 0))
    editor = utils.Button("Level Editor", font, 512, 400, (200, 0, 0))
    options = utils.Button("Options", font, 512, 500, (200, 0, 0))

    while running:
        clock.tick(60)  # limit FPS to 60
        screen.blit(background.image, (0, 0))
        screen.blit(title, titlepos)
        start_game.update()
        exit_game.update()
        editor.update()
        level_select.update()
        curseur.update()
        options.update()
        utils.update_music_menu()

        for AI_sprite in AI_group:
            AI_sprite.update(MAIN_PATH, curseur.rect.center,
                             walls_group, pits_group, [], in_menu=True)

        pygame.display.flip()

        for event in pygame.event.get():
            # if player wants to quit (using window buttons)
            if event.type == pygame.QUIT:
                running = 0
                pygame.mixer.music.fadeout(200)
                clock.tick(5)
                pygame.quit()

            # player clicked somewhere
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

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
                    pygame.display.set_caption(settings.GAME_NAME)

                # player clicked on "Level Selection"
                elif level_select.highlighten:
                    clickSound.play()
                    if not level_selection_menu():
                        running = 0
                        pygame.quit()
                    else:
                        pygame.display.set_caption(settings.GAME_NAME)

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
