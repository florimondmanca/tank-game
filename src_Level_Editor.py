# Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Level editor

## Imports

from tkinter import *
import math
import sys
import os
join = os.path.join

#chemin d'accès aux fichiers

path = os.getcwd()

## Variables globales 

edit_path = join(path, "custom_levels")
int_matrix = [[0 for j in range(32)] for i in range(21)]
IA = [] #liste correspondant aux IA blue, bluePlus, purple et purplePlus
paths_matrix= []
rect_matrix= [[None for j in range(32)] for i in range(21)]
color_dict = { 'white': ('#fff',0) , 'black': ('#000',1), 'brown': ('#a60',2),
           'green': ('#0f0',3) , 'yellow' : ('#ff0',4) , 'orange': ('#fc0',5),
           'blue': ('#00f',6), 'darkblue' : ('#00a',7) , 'red': ('#f00',8), 'darkred' : ('#c00', 9) ,  
           'purple':('#f0f',10) , 'darkpurple' : ('#a0a' , 11) , 'grey' : ('#aaa' , 12), 'darkgrey' : ('#777', 13) }
type_dict = { 'white': 'None', 'black': 'Wall', 'brown': 'Pit',
          'green': 'Player', 'yellow': 'IA Yellow', 'orange': 'IA YellowPlus',
          'blue': 'IA Blue', 'darkblue' : 'IA BluePlus', 'red': 'IA Red', 'darkred' : 'IA redPlus',
        'purple': 'IA purple','darkpurple' : 'IA PurplePlus' , 'grey' : "Spawner", 'darkgrey' : "SpawnerPlus"}

## UTILITAIRES

def convert(liste, split=False) : #renvoie la chaine de caractère correspondant à la liste avec des espaces
    string = ""
    if not split :
        for i in range(len(liste)) :
            string+= str(liste[i])+" "
    else : #split = True, la liste est une liste de tupple qu'il faut séparer
        for i in range((len(liste))) :
            string+= str(liste[i][0])+" "+ str(liste[i][1])+" "
    return string+'\n'

def create_level(matrice, paths) :
    n=1
    while os.path.exists(join(edit_path , "custom_level"+str(n)+".txt")):
        n+=1
    fname = "custom_level"+str(n)+".txt"
    fullname = join(edit_path, fname)
    file = open(fullname, 'w')
    for i in range(len(matrice)) :
          file.write(convert(matrice[i]))
    if paths != [] :
        for i in range(len(paths)) :
            file.write(convert(paths[i], split=True))
    file.close()

def convert_and_sort(matrix) : #liste de liste de way_points -> liste de x1 y1 x2 y2 ...
    sortie = []
    for i in range(len(matrix)):
        sortie.append(matrix[i])
        for j in range(len(matrix[i])):
            (a,b) = matrix[i][j].pos
            sortie[i][j] = (b,a)
    sortie.sort() #on trie les listes de la matrice
    for i in range(len(sortie)):
        for j in range(len(sortie[i])):
            (a,b) = sortie[i][j]
            sortie[i][j] = (b,a)
    return sortie

def export(zone_dessin, int_matrix, paths_matrix, IA):
    warn = Tk()
    warn.title("Warning")
    
    texte=Label(warn, text="You won't be able to edit this level after its exportation")
    texte.pack()
    
    back = Button(warn,text='Get back to work', command=warn.destroy)
    back.pack(side=LEFT)
    
    def fct(zone_dessin, int_matrix, paths_matrix, IA):
        create_level(int_matrix,convert_and_sort(paths_matrix))
        clear(zone_dessin, int_matrix, paths_matrix, IA)
        warn.destroy()
        
    exp = Button(warn, text = 'Continue', command=lambda: fct(zone_dessin, int_matrix, paths_matrix, IA))
    exp.pack(side = RIGHT)
    warn.mainloop()

def clear(zone_dessin, int_matrix, paths_matrix, IA): #réinitialise l'éditeur de niveau
    int_matrix = [[0 for j in range(32)] for i in range(21)]
    paths_matrix= []
    IA = []
    for i in range(21) :
        for j in range(32) :
            if i==0 or i==20 or j==0 or j==31 : #on est sur les bords
                rect = rectangle(zone_dessin, i, j, 'black', color_dict)
                rect_matrix[i][j] = rect
                int_matrix[i][j] = color_dict['black'][1]
            else :
                rect = rectangle(zone_dessin, i, j, 'white', color_dict)
                rect_matrix[i][j] = rect
                int_matrix[i][j] = color_dict['white'][1]
        
def clear_paths(paths_matrix, zone_dessin, IA) : #réinitialise uniquement les chemins liés aux IA
    paths_matrix = []
    for i in range(len(IA)) :
        paths_matrix.append([])
        zone_dessin.delete(("path",str(i)))
    for x in IA :
        x.points_list = [way_point(zone_dessin,x.pos[1],x.pos[0],x.id)]

## GESTION D'EVENEMENTS LIES A LA SOURIS

class mouse():
    ''' la classe qui gère toutes les actions du curseur dans l'interface Tkinter'''
    def __init__(self,fenetre,color='white'):
        self.color = color
        self.mode = 'normal'
        self.where = fenetre
        self.buttons = None
        self.selected = None # le rectangle de l'IA bleue sélectionnée
    
    # les fonctions d'état
    
    def mouse_normal(self, zone_dessin):
        # passe la souris en mode normal à l'appui sur le bouton 'Normal mode'
        self.mode = 'normal'
        self.selected = None
        zone_dessin.delete("paths")

    def mouse_path_creation(self, zone_dessin):
        # passe la souris en mode de création de path pour IA bleue à
        # l'appui sur le bouton 'Path creation mode'
        self.mode = 'path_creation'
        for x in IA:
            pts = x.points_list
            for i in range(len(pts)-1) :
                pts[i].plot(zone_dessin)
                pts[i].bind(pts[i+1], zone_dessin)
    
    def In_Outils(self, event):
        self.where = "zone_outils"
    def Out(self, event):
        self.where = None
    def In_Dessin(self, event):
        self.where = "zone_dessin"

    ## les fonctions d'édition
    
    def mouse_color_click(self, event):
    # permet de donner à la souris la couleur qui a été choisie
        for button in self.buttons:
            if button.selected :
                button.highlight_button() #on enlève la précédente selection
            if (event.x//25,event.y//25) == button.pos:
                self.color = button.color
                self.mode = 'normal' #on repasse en mode normal
                button.highlight_button()

    def print_color(self, event, zone_dessin, int_matrix, paths_matrix, color_dict, IA):

    # permet en mode normal de déposer sur le canevas un rectangle de couleur self.color
    # permet en mode création de chemin de dessiner le chemin de la dernière IA sélectionnée
        j , i = event.x//25 , event.y//25
        
        if 1<=i<=19 and 1<=j<=30: # on ne doit pas changer les murs extérieurs
            rect = rect_matrix[i][j]
            
            # Cas 1: on est en mode normal d'édition
            if self.mode == 'normal':
                if rect.color != self.color:
                    if self.color == 'blue' or self.color == 'darkblue'  or self.color == 'purple' or  self.color == 'darkpurple' : #on a affaire à une IA necessitant un path 
                        newIA = IA_rectangle(zone_dessin,i,j,self.color, zone_dessin, color_dict)
                        rect_matrix[i][j] = newIA
                        int_matrix[i][j] = color_dict[self.color][1]
                        newIA.id = len(IA)
                        IA.append(newIA)
                        paths_matrix.append([])
                    else :
                        rect_matrix[i][j] = rectangle(zone_dessin,i,j,self.color, color_dict)
                        int_matrix[i][j] = color_dict[self.color][1]
                
            # Cas 2: on est en mode création de chemin d'IA bleue
            if self.mode == 'path_creation' :
                n = int_matrix[i][j]
                if n == 6 or n==7 or n==10 or n==11 : #on a affaire à une IA qui nécessite un path
                    for x in IA :
                        if x.selected :
                            x.highlight_rect(zone_dessin) #on deselectionne toutes les IA
                        cwia = rect_matrix[i][j]
                        self.selected = cwia.id
                        cwia.highlight_rect(zone_dessin)
                elif self.selected != None :
                    cwia = IA[self.selected]
                    pt=way_point(zone_dessin,i,j,cwia.id)
                    pt.bind(cwia.points_list[-1], zone_dessin)
                    pt.plot(zone_dessin)
                    cwia.points_list.append(pt)
                    paths_matrix[cwia.id] = cwia.points_list
                    
    def mouse_click_left(self, event, zone_dessin, int_matrix, paths_matrix, color_dict, IA):
        if self.where == 'zone_dessin':
            self.print_color(event, zone_dessin, int_matrix,  paths_matrix, color_dict, IA) # on effectue l'action de la zone de dessin
        elif self.where == 'zone_outils':
            self.mouse_color_click(event) #on effecture l'action de la zone des outils

    def mouse_click_right(self, event, zone_dessin, int_matrix, rect_matrix, paths_matrix, color_dict, number):
    #N'est activée que dans la zone de dessin (contrairement au clic gauche)
        if  self.where=="zone_dessin" :
            
            if self.mode == 'normal' :    #En mode normal, permet d'effacer le rectangle sur lequel pointe la souris
                j , i = event.x//25 , event.y//25
                if 1<=i<=19 and 1<=j<=30: # on ne doit pas changer les murs extérieurs
                    rect = rect_matrix[i][j]
                if self.mode == 'normal' :
                    rect_matrix[i][j] = rectangle(zone_dessin,i,j, "white", color_dict)
                    int_matrix[i][j] = 0
        
            elif self.mode == 'path_creation' : #En mode path_creation, permet d'enlever un point du chemin
                if self.selected != None :
                    cwia = IA[self.selected]
                    pts = cwia.points_list
                    if (len(pts))>1 :
                        pts.pop()
                        cwia.points_list = pts
                        paths_matrix[cwia.id] = pts
                        zone_dessin.delete(("paths",str(cwia.id)))
                        for i in range(len(pts)-1) :
                            pts[i].plot(zone_dessin)
                            pts[i].bind(pts[i+1], zone_dessin)
                    
         
## CLASSES DIVERSES

class rectangle():
    '''regroupe un rectangle du canevas, sa couleur et sa position'''
    def __init__(self, can, i, j, color, color_dict):
        rect = can.create_rectangle(25*j , 25*i , 25*(j+1) , 25*(i+1) ,
                            width=1, fill= color_dict[color][0], outline= "black")
        self.rect = rect
        self.color = color
        self.pos = (j,i)
        self.master = can
        self.selected = False
    
class IA_rectangle:
    ''' un rectangle d'une IA bleue. Contient, en plus d'un rectangle classique, le parcours de l'IA'''
    def __init__(self, can, i, j, color, zone_dessin, color_dict):
        rect = can.create_rectangle(25*j , 25*i , 25*(j+1) , 25*(i+1) ,
                            width=1, fill= color_dict[color][0], outline= "black")
        self.rect = rect
        self.color = color
        self.pos = (j,i)
        self.master = can
        self.id = -1
        self.selected = False
        self.points_list = [way_point(zone_dessin,i,j,self.id)] #liste d'objets de classe way_point formant le chemin suivi

    def highlight_rect(self, zone_dessin) :
        can = self.master
        j,i = self.pos
        color=self.color
        if not self.selected :
            self.rect = can.create_rectangle(25*j , 25*i , 25*(j+1) , 25*(i+1) , width=1, fill= color_dict[color][0], outline= "#fe2")
            self.points_list[0] = way_point(zone_dessin, i, j, self.id)
        else :
            self.rect = can.create_rectangle(25*j , 25*i , 25*(j+1) , 25*(i+1), width=1, fill = color_dict[color][0], outline='black')
            self.points_list[0] = way_point(zone_dessin,i,j,self.id)
        self.selected = not self.selected

class way_point():
    def __init__(self, can, i, j, n):
        rect = can.create_rectangle(25*j+5 , 25*i+5 , 25*(j+1)-5 , 25*(i+1)-5 ,
                                    width=1, fill= "#aaa", outline= "#000", tag = ("path",str(n)))
        self.id = n
        self.rect = rect
        self.color = "#aaa"
        self.pos = (j,i)

    def bind(self, wp, zone_dessin) : #trace une ligne entre deux waypoints
        (j1,i1)= self.pos
        (j2,i2)= wp.pos
        x1,y1,x2,y2= 25*j1+12 , 25*i1+12 , 25*j2+12 , 25*i2+12
        if abs(x1-x2) > abs(y1-y2):
                zone_dessin.create_line(x1,y1,x2,y1, x2,y2, fill = "#aaa", width = 1, tag = ("path",str(self.id)))
        else :
            zone_dessin.create_line(x1,y1,x1,y2, x2,y2, fill = "#aaa", width = 1, tag = ("path",str(self.id)))
        
    def plot(self, zone_dessin):
        (j,i) = self.pos
        zone_dessin.create_rectangle(25*j+8,25*i+8,25*(j+1)-8,25*(i+1)-8, tag=("path",str(self.id)))

class color_button:
    # classe des boutons-outil
    def __init__(self, can, x1, y1, x2, y2, color, color_dict, type_dict):
        rect, text = self.create_button(can, x1, y1, x2, y2, color, color_dict, type_dict)
        self.rectangle = rect
        self.pos = (x1//25,y1//25)
        self.master= can
        self.coords= (x1,y1,x2,y2)
        self.text = text
        self.color = color
        self.selected = False

    def create_button(self, can, x1, y1, x2, y2, color, color_dict, type_dict):
        rect = can.create_rectangle(x1,y1,x2,y2, width=1, fill = color_dict[color][0], outline='black')
        text = can.create_text(x2+4,(y1+y2)/2, text=type_dict[color], anchor=W)
        return rect, text
    
    def highlight_button(self) :
        can = self.master
        x1,y1,x2,y2 = self.coords
        color=self.color
        if not self.selected :
            self.rectangle = can.create_rectangle(x1,y1,x2,y2, width=1, fill = color_dict[color][0], outline='#ee2')
        else :
            self.rectangle = can.create_rectangle(x1,y1,x2,y2, width=1, fill = color_dict[color][0], outline='black')
        self.selected = not self.selected


## LA FONCTION PRINCIPALE

def level_editor():
    
    fenetre = Tk()
    fenetre.title("Tank Game Level Editor")
    
    # la souris
    souris = mouse(fenetre)
    fenetre.bind("<Button-1>", lambda event: souris.mouse_click_left(event, zone_dessin, int_matrix, paths_matrix, color_dict, IA))
    fenetre.bind("<Button-3>", lambda event: souris.mouse_click_right(event, zone_dessin, int_matrix, rect_matrix, paths_matrix, color_dict, IA))
    bout = Button(fenetre,text='Exit',command=lambda: fenetre.destroy())
    bout.pack()
    
    # la fenetre de boutons d'action
    fenetre_divers = LabelFrame(fenetre,text="Options")
    fenetre_divers.pack(side=RIGHT)
    b_normal = Button(fenetre_divers, text="Normal mode", command=lambda: souris.mouse_normal(zone_dessin))
    b_normal.pack()
    b_path = Button(fenetre_divers, text="Path creation mode", command=lambda: souris.mouse_path_creation(zone_dessin))
    b_path.pack()
    exporter = Button(fenetre_divers,text="Export",command=lambda: export(zone_dessin, int_matrix, paths_matrix, IA))
    exporter.pack()
    clear_all = Button(fenetre_divers, text = "Clear All" , command=lambda: clear(zone_dessin, int_matrix, paths_matrix, IA))
    clear_all.pack()
    clear_p = Button(fenetre_divers, text = "Clear Paths", command=lambda: clear_paths(paths_matrix, zone_dessin, IA))
    clear_p.pack()
    
    # la fenetre de boutons-outil
    fenetre_outils = LabelFrame(fenetre, text="Outils")
    fenetre_outils.bind("<Button-1>", souris.mouse_color_click)
    fenetre_outils.bind("<Enter>", souris.In_Outils)
    fenetre_outils.bind("<Leave>", souris.Out)
    fenetre_outils.pack(side=LEFT)
    zone_outils=Canvas(fenetre_outils, width=120, height=525)
    zone_outils.pack()
    
    # la fenetre de dessin
    fenetre_dessin = LabelFrame(fenetre, text="Map")
    fenetre_dessin.bind("<Enter>", souris.In_Dessin)
    fenetre_dessin.bind("<Leave>", souris.Out)
    fenetre_dessin.pack(side=RIGHT)
    zone_dessin = Canvas(fenetre_dessin, width = 800, height = 525)
    zone_dessin.pack()
    
    # création des boutons-outil dans le canevas zone_outils
    
    buttons = []
    for color in color_dict:
        n = color_dict[color][1]
        button = color_button(zone_outils,4, 25*(n+1), 4+25, 25*(n+2), color, color_dict, type_dict)
        buttons.append(button)
    souris.buttons = buttons

    # creation des rectangles et initialisation de la matrice
    
    for i in range(21) :
        for j in range(32) :
            if i==0 or i==20 or j==0 or j==31 : #on est sur les bords
                rect = rectangle(zone_dessin, i, j, 'black', color_dict)
                rect_matrix[i][j] = rect
                int_matrix[i][j] = color_dict['black'][1]
            else :
                rect = rectangle(zone_dessin, i, j, 'white', color_dict)
                rect_matrix[i][j] = rect
                int_matrix[i][j] = color_dict['white'][1]
    
    
    #boucle principale
    fenetre.mainloop()
    fenetre.destroy()

if __name__ == "__main__":
    level_editor()