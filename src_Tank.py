# Tank Game:
# A game with tanks and stuff.
#
# by Erkalys & Florimond Manca
#
# Defining the base Tank class

# Imports

import pygame
from pygame.locals import *
import math
import os
from src import utils
from src.bullet_cursor import Bullet

path = os.getcwd()
join = os.path.join

if '\\' in path:
    path = path.replace('\\scripts', '')
elif '/' in path:
    path = path.replace('/scripts', '')


# Note: All angles defined in these classes (Tank, Canon, Bullet...) are
# defined from the x axis and anti-clockwise.

class Body(pygame.sprite.Sprite):
    """Body: the body of a tank."""

    def __init__(self, path, tank_name, canon_name, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(path, tank_name)
        self.imageBase = self.image
        self.area = pygame.display.get_surface().get_rect()
        self.speed = 1
        self.rect.center = pos
        self.movepos = [0, 0]    # moving speed right/left, up/down
        self.angle = math.radians(0)   # initial angle of the body
        self.goal_angle = 0            # initial goal angle of the body
        self.rotation_step = math.radians(7.5)  #
        self.path = path

    def _update_body_angle(self):
        '''_update_body_angle(self): Gère la rotation du corps du tank. Incrémente ou décrémente son angle suivant la valeur de l'angle de consigne goal_angle, obtenu à partir des touches directionnelles du clavier. '''
        alpha, beta = round(math.degrees(self.angle)), self.goal_angle
        delta = beta - alpha
        if delta > 180:       # gère les cas particuliers
            delta = delta - 360
        if delta < -180:
            delta = delta + 360
        if delta > 5:       # on se laisse une marge pour éviter les erreurs numériques
            self.angle += self.rotation_step
        elif delta < -5:
            self.angle -= self.rotation_step

    def _rotate_body_image(self):
        ''' _rotate_body_image(self): pivote le sprite du corps d'un angle self.angle '''
        center_rect = self.rect.center
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.imageBase, angle)
        self.rect = self.image.get_rect(center=center_rect)

    def update(self, walls_group=None):
        """update(self, walls_group): updates the body's position, taking walls into account"""
        if walls_group is None:
            walls_group = pygame.sprite.Group()
        self._update_body_angle()
        self._rotate_body_image()
        move_x = self.movepos[0]
        move_y = self.movepos[1]
        oldpos = self.rect
        self.rect = self.rect.move(move_x, move_y)
        collided_walls = pygame.sprite.spritecollide(
            self, walls_group, False, pygame.sprite.collide_rect)
        if collided_walls:
            n = len(collided_walls)
            self.rect = oldpos
            # on trouve la direction à bloquer
            for wall in collided_walls:
                if wall.rect.collidepoint(self.rect.midright):
                    if self.movepos[0] == 1:
                        move_x = 0
                if wall.rect.collidepoint(self.rect.midleft):
                    if self.movepos[0] == -1:
                        move_x = 0
                if wall.rect.collidepoint(self.rect.midtop):
                    if self.movepos[1] == -1:
                        move_y = 0
                if wall.rect.collidepoint(self.rect.midbottom):
                    if self.movepos[1] == 1:
                        move_y = 0
            self.rect = self.rect.move(move_x, move_y)
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)

    # fonctions de déplacement
    def moveright(self):
        self.movepos[0] = self.speed

    def moveleft(self):
        self.movepos[0] = -self.speed

    def moveup(self):
        self.movepos[1] = -self.speed

    def movedown(self):
        self.movepos[1] = self.speed

    def stophorizontal(self):
        self.movepos[0] = 0

    def stopvertical(self):
        self.movepos[1] = 0

    def stop(self):
        self.movepos = [0, 0]

    def bullet_angle(self, target_pos):
        ''' bullet_angle(self, target_pos): calcule l'angle de la trajectoire du nouveau boulet.
        target_pos représente la position de la cible'''
        distance_x = self.rect.centerx - target_pos[0]
        distance_y = self.rect.centery - target_pos[1]
        return math.atan2(distance_x, distance_y) + math.pi / 2


class Canon(pygame.sprite.Sprite):
    """Canon: the canon of a tank."""

    def __init__(self, path, canon_name, pos, target_pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(path, canon_name)
        self.imageBase = self.image
        self.rect.center = pos
        self.angle = math.radians(-90)
        if target_pos != None:
            self._rotate(target_pos)

    def _rotate(self, target_pos):
        """Rotates the canon's sprite."""
        distance_x = self.rect.centerx - target_pos[0]
        distance_y = self.rect.centery - target_pos[1]
        self.angle = math.atan2(distance_x, distance_y) + math.pi
        centre_rect = self.rect.center
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.imageBase, angle)
        self.rect = self.image.get_rect(center=centre_rect)

    def update(self, pos, target_pos):
        self.rect.center = pos
        self._rotate(target_pos)
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)


class Tank:
    """Tank: the tank used by the player and the AI's. Consists of a Body and a Canon."""

    def __init__(self, path, tank_name, canon_name, pos, target_pos=None):
        self.body = Body(path, tank_name, canon_name, pos)
        self.canon = Canon(path, canon_name, pos, target_pos)
        self.bullets = pygame.sprite.Group()
        self.alive = True

    def create_bullet(self, path, target_pos):
        beta = self.body.bullet_angle(target_pos)
        x_bullet, y_bullet = self.body.rect.center
        x_bullet += int(30 * math.cos(beta))   # prend en compte
        y_bullet += int(-30 * math.sin(beta))  # la dimension du rect.
        created_bullet = Bullet(
            os.path.join(path, 'images'), x_bullet, y_bullet, beta)
        self.bullets.add(created_bullet)
        return created_bullet

    def move(self, right, left, up, down):
        # Case 1: right was hit and left was not
        if right and not left:
            self.body.moveright()
            # deal with up and down keys
            if up and not down:
                self.body.goal_angle = 45
            elif down and not up:
                self.body.goal_angle = -45
            else:
                self.body.goal_angle = 0

        # Counter-case 1: left was hit and right was not
        elif left and not right:
            self.body.moveleft()
            if up and not down:
                self.body.goal_angle = 135
            elif down and not up:
                self.body.goal_angle = -135
            else:
                self.body.goal_angle = 180

        # Case 2: up was hit and down was not
        if up and not down:
            self.body.moveup()
            if right and not left:
                self.body.goal_angle = 45
            elif left and not right:
                self.body.goal_angle = 135
            else:
                self.body.goal_angle = 90

        # Counter-case 2: down was hit and up was not
        elif down and not up:
            self.body.movedown()
            if right and not left:
                self.body.goal_angle = -45
            elif left and not right:
                self.body.goal_angle = -135
            else:
                self.body.goal_angle = -90

        # Case 3: stop cases
        if (not right and not left) or (right and left):
            self.body.stophorizontal()
        if (not up and not down) or (up and down):
            self.body.stopvertical()
        if not right and not left and not up and not down:
            self.body.stop()

    def update(self, path, target_pos, bullets_group, walls_group=None):
        destroyedSound = pygame.mixer.Sound(
            join(join(path, "music"), "destroyed_sound.wav"))
        v = utils.get_volumes()[1]
        destroyedSound.set_volume(v)
        if self.alive:
            for bullet in bullets_group:
                if pygame.sprite.collide_rect(bullet, self.body):
                    # le boulet a percuté le tank
                    bullet.kill()
                    destroyedSound.play()
                    self.alive = False
                    break
            self.body.update(walls_group)
            screen = pygame.display.get_surface()
            screen.blit(self.body.image, self.body.rect)
            self.canon.update(self.body.rect.center, target_pos)
        else:
            screen = pygame.display.get_surface()
            screen.blit(self.body.image, self.body.rect)
