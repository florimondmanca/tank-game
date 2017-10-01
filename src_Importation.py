## Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Defining the data import functions.

import pygame
from pygame.locals import *
import sys
import os
from src_Walls import *

path = os.getcwd().replace("/scripts", "")
join = os.path.join


def get_voisins(T, i, j, p):
    """ Renvoie les voisins (valeur p) de l"élément T[i][j] """
    n, m = len(T), len(T[0])
    # voisins est constituée de chaines de caractères définissant où se situent
    # les murs voisins de la case (i,j) considérée.
    if i == 0 :
        if j == 0:      # si sur le coin en haut à gauche
            voisins = [(T[i][j + 1], "droite"),
                       (T[i + 1][j], "bas")]
        elif j == m-1:  # si sur le coin en haut à droite
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i + 1][j], "bas")]
        else:           # si en haut
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i][j + 1], "droite"),
                       (T[i + 1][j], "bas")]
    elif i == n-1 :
        if j == 0:      # si sur le coin en bas à gauche
            voisins = [(T[i - 1][j], "haut"),
                       (T[i][j + 1], "droite")]
        elif j == m-1:  # si sur le coin en bas à droite
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i - 1][j], "haut")]
        else:           # si en bas
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i][j + 1], "droite"),
                       (T[i - 1][j], "haut")]
    else :
        if j == 0:
            voisins = [(T[i][j + 1], "droite"),
                       (T[i + 1][j], "bas"),
                       (T[i - 1][j], "haut")]
        elif j == m-1:
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i + 1][j], "bas"),
                       (T[i - 1][j], "haut")]
        else:
            voisins = [(T[i][j - 1], "gauche"),
                       (T[i][j + 1], "droite"),
                       (T[i - 1][j], "haut"),
                       (T[i + 1][j], "bas")]
    voisins = [v[1] for v in voisins if v[0] == p]
    return voisins

def get_type(object_type, voisins):
    # consider all the possible cases.
    n = len(voisins)
    if n == 0:
        return "{}_square.png".format(object_type)
    if n == 1:
        pos = voisins[0]
        if pos == "haut":
            return "{}_edge_B.png".format(object_type)
        elif pos == "bas":
            return "{}_edge_T.png".format(object_type)
        elif pos == "droite":
            return "{}_edge_R.png".format(object_type)
        elif pos == "gauche":
            return "{}_edge_L.png".format(object_type)
    elif n == 2:
        pos = voisins[0] , voisins[1]
        if "haut" in pos and "bas" in pos:
            return "{}_vertical.png".format(object_type)
        elif "gauche" in pos and "droite" in pos:
            return "{}_horizontal.png".format(object_type)
        elif "bas" in pos and "droite" in pos:
            return "{}_cornerBR.png".format(object_type)
        elif "haut" in pos and "droite" in pos:
            return "{}_cornerTR.png".format(object_type)
        elif "bas" in pos and "gauche" in pos:
            return "{}_cornerBL.png".format(object_type)
        elif "haut" in pos and "gauche" in pos:
            return "{}_cornerTL.png".format(object_type)
    elif n == 3:
        pos = [voisins[0], voisins[1], voisins[2]]
        if "bas" not in pos:
            return "{}_T_B.png".format(object_type)
        elif "gauche" not in pos:
            return "{}_T_L.png".format(object_type)
        elif "haut" not in pos:
            return "{}_T_T.png".format(object_type)
        elif "droite" not in pos:
            return "{}_T_R.png".format(object_type)
    elif n== 4:
        return "{}_X.png".format(object_type)
    else:
        return None
    
def get_level(path, n, custom=False): # n est le numéro du niveau à charger. -1 pour le menu. Si custom est True, on va chercher un niveau custom
    screen = pygame.display.get_surface()
    if n == -1:
        level_path = join(path, join("levels", "menu.txt"))
    else:
        if custom:
            level_path = join(path, join("custom_levels", "custom_level{}.txt".format(n)))
        else:
            level_path = join(path, join("levels","level{}.txt".format(n)))

    with open(level_path, mode="r") as texte:
        map_niveau = []
        
        # on remplit d"abord la matrice des murs, on récupère
        # le placement des IA, etc.

        for i in range(21):
            map_niveau.append(texte.readline().strip().split())
            for j in range(32):
                map_niveau[i][j] = int(map_niveau[i][j])

        walls_group = pygame.sprite.Group()
        pits_group = pygame.sprite.Group()
        pos_player = (0,0)
        pos_AI = []
        for i in range(21):
            for j in range(32):
                pos = (32*j,32*i)
                var = map_niveau[i][j]
                if var == 1:
                    typemur = get_type("wall", get_voisins(map_niveau, i, j, 1))
                    walls_group.add(Wall(path, typemur, i, j))
                elif var == 2:
                    typemur = get_type("pit",  get_voisins(map_niveau, i, j, 2))
                    pits_group.add(Pit( path, typemur, i, j ))
                else:
                    # on prend en compte l"offset pour les tanks
                    pos = (32*j+16, 32*i+16)
                    if var == 3: pos_player = pos
                    if var == 4: pos_AI.append( ["yellow", pos])
                    elif var == 5: pos_AI.append( ["yellowPlus", pos])
                    elif var == 6: pos_AI.append( ["blue",pos] )
                    elif var == 7: pos_AI.append( ["bluePlus",pos] )
                    elif var == 8: pos_AI.append(["red" , pos])
                    elif var == 9: pos_AI.append(["redPlus" , pos])
                    elif var == 10: pos_AI.append(["purple" , pos])
                    elif var == 11: pos_AI.append(["purplePlus", pos])
                    elif var == 12: pos_AI.append(["spawner" , pos])
                    elif var == 13: pos_AI.append(["spawnerPlus", pos])

        # on obtient ensuite la liste des déplacements des IA bleues
        
        n_blues = len( [IA for IA in pos_AI if IA[0] == "blue" or IA[0] == "bluePlus" or IA[0] == "purple" or IA[0] == "purplePlus"] )
        
        liste_dep = texte.readline().strip().split()
        # list_dep contient la liste non-organisée en tuples des coordonnées des
        # points à atteindre : x1 y1 x2 y2 x3 y3 etc.
        
        points_list = [] # contiendra l"ensemble des trajectoires des IA du niveau

        for k in range(n_blues):  #d"abord les IA bleues
            liste = []
            for i in range(len(liste_dep)//2):
                liste.append((32*int(liste_dep[0])+16, 32*int(liste_dep[1])+16))
                liste_dep.pop(0)
                liste_dep.pop(0)
            points_list.append(liste)
            liste_dep = texte.readline().strip().split()

    return walls_group, pits_group, pos_player, pos_AI, points_list

def init_unlocked(a_bool):
    unlock_path = join(path, "unlocked.txt")
    with open(unlock_path,mode="w") as texte:
        n = 1
        while os.path.exists(join(join(path, "levels"), "level{}.txt".format(n))):
            n += 1
        string = "1 1 "
        for i in range(1, n) :
            if not a_bool: string += "0 "
            else : string += "1 "
        texte.write(string)

def get_unlocked():
    unlock_path = join(path, "unlocked.txt")
    with open(unlock_path, mode="r") as texte:
        liste = texte.readline().strip().split()
    return [int(x) for x in liste]
	#liste[i] permet de savoir si le niveau i est débloqué ou non. Liste[0] est inutile

def overwrite_unlocked(liste):
    unlock_path = join(path, "unlocked.txt")
    with open(unlock_path, mode = "w") as texte:
        texte.write(" ".join(str(x) for x in liste))
    
