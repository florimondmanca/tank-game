"""Base Tank class."""
# Imports

import pygame
import math
import os
from src import utils
from src.bullet_cursor import Bullet
from . import settings

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

    def __init__(self, image_name, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image_name)
        self.base_image = self.image
        self.area = pygame.display.get_surface().get_rect()
        self.speed = 1
        self.rect.center = pos
        self.move_x = 0
        self.move_y = 0
        self.angle = 0
        self.goal_angle = 0
        self.rotation_step = math.radians(7.5)

    def _update_body_angle(self):
        """Update the tank's body angle.

        Increment or decrement the angle according to the goal_angle,
        which is obtained through keyboard directional keys.

        Let α be the body's current angle, and γ the goal angle.
        Compute δ = (γ - α)
        Transform δ = (δ % 360)
        """
        # TODO refactor
        alpha, beta = round(math.degrees(self.angle)), self.goal_angle
        delta = beta - alpha
        if delta > 180:  # gère les cas particuliers
            delta = delta - 360
        if delta < -180:
            delta = delta + 360
        _eps = 5  # margin for numerical errors
        if delta > _eps:
            self.angle += self.rotation_step
        elif delta < -_eps:
            self.angle -= self.rotation_step

    def _rotate_body_image(self):
        """Rotate the body's sprite according to self.angle."""
        center_rect = self.rect.center
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect(center=center_rect)

    def update(self, walls_group=None):
        """Update the body's position, taking walls into account."""
        if walls_group is None:
            walls_group = pygame.sprite.Group()
        self._update_body_angle()
        self._rotate_body_image()
        oldpos = self.rect
        move_x, move_y = self.move_x, self.move_y
        self.rect = self.rect.move(move_x, move_y)
        collided_walls = pygame.sprite.spritecollide(
            self, walls_group, False, pygame.sprite.collide_rect)
        if collided_walls:
            self.rect = oldpos
            # find the direction to block
            for wall in collided_walls:
                if wall.rect.collidepoint(self.rect.midright):
                    if self.move_x > 0:
                        move_x = 0
                if wall.rect.collidepoint(self.rect.midleft):
                    if self.move_x < 0:
                        move_x = 0
                if wall.rect.collidepoint(self.rect.midtop):
                    if self.move_y < 0:
                        move_y = 0
                if wall.rect.collidepoint(self.rect.midbottom):
                    if self.move_y > 0:
                        move_y = 0
            self.rect = self.rect.move(move_x, move_y)
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)

    def moveright(self):
        self.move_x = self.speed

    def moveleft(self):
        self.move_x = -self.speed

    def moveup(self):
        self.move_y = -self.speed

    def movedown(self):
        self.move_y = self.speed

    def stophorizontal(self):
        self.move_x = 0

    def stopvertical(self):
        self.move_y = 0

    def stop(self):
        self.move_x = self.move_y = 0

    def bullet_angle(self, target_pos):
        """Compute the angle of trajectory for a new bullet.

        Parameters
        ----------
        target_pos : tuple
            The 2D position of the target.
        """
        distance_x = self.rect.centerx - target_pos[0]
        distance_y = self.rect.centery - target_pos[1]
        return math.atan2(distance_x, distance_y) + math.pi / 2


class Canon(pygame.sprite.Sprite):
    """Canon: the canon of a tank."""

    def __init__(self, image_name, pos, target_pos=None):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(image_name)
        self.base_image = self.image
        self.rect.center = pos
        self.angle = math.radians(-90)
        if target_pos is not None:
            self._rotate(target_pos)

    def _rotate(self, target_pos):
        """Rotate the canon's sprite to look at a target position."""
        distance_x = self.rect.centerx - target_pos[0]
        distance_y = self.rect.centery - target_pos[1]
        self.angle = math.atan2(distance_x, distance_y) + math.pi
        centre_rect = self.rect.center
        angle = math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.base_image, angle)
        self.rect = self.image.get_rect(center=centre_rect)

    def update(self, pos, target_pos):
        self.rect.center = pos
        self._rotate(target_pos)
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)


class Tank:
    """A Tank consisting of a Body and a Canon.

    Class attributes
    ----------------
    body_image_name : str
        Filename of the tank's body image.
        Default is DEFAULT_TANK_BODY_IMAGE.
    canon_image_name : str
        Filename of the tank's canon image.
        Default is DEFAULT_TANK_CANON_IMAGE.
    fire_sound_name : str
        Filename of the tank's firing sound.
        Default is DEFAULT_TANK_FIRE_SOUND.
    """

    body_image_name = settings.DEFAULT_TANK_BODY_IMAGE
    canon_image_name = settings.DEFAULT_TANK_CANON_IMAGE
    fire_sound_name = settings.DEFAULT_TANK_FIRE_SOUND

    def __init__(self, pos, target_pos=None):
        self.body = Body(self.body_image_name, pos)
        self.canon = Canon(self.canon_image_name, pos, target_pos)
        self.fire_sound = utils.load_sound(self.fire_sound_name)
        self.bullets = pygame.sprite.Group()
        self.alive = True

    def create_bullet(self, path, target_pos):
        beta = self.body.bullet_angle(target_pos)
        x_bullet, y_bullet = self.body.rect.center
        x_bullet += int(30 * math.cos(beta))   # prend en compte
        y_bullet += int(-30 * math.sin(beta))  # la dimension du rect.
        created_bullet = Bullet(x_bullet, y_bullet, beta)
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
        destroyedSound = utils.load_sound("destroyed_sound.wav")
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
