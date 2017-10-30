"""
Tank Game: A game with tanks and stuff.

by Erkalys & Florimond Manca

Defining AI and Player classes
"""

# Imports

import pygame
import math
import os
from queue import PriorityQueue  # Priority Queue for A* algorithm
from random import randint
from src.tank import Tank
from src import utils

path = os.getcwd()
join = os.path.join

# Classes Player, YellowAI, BlueAI, RedAI, PurpleAI, Spawner


def plussify(cls):
    """Return the plussified version of tank_cls.

    Example:
    BluePlusAI = plussify(BlueAI)
    """
    class plussified_class(cls, YellowPlusAI):

        def __init__(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)
            self.updater_class = YellowPlusAI
    return plussified_class


class Player(Tank):
    """Player: the tank controlled by the player."""

    def __init__(self, pos):
        Tank.__init__(self, pos)
        self.score = 0    # player's score
        self.fire_sound.set_volume(utils.get_volumes()[1])


class YellowAI(Tank):
    """YellowAI: A still AI that shoots the player on sight."""

    body_image_name = "tank_corps_yellow.png"
    canon_image_name = "canon_yellow.png"

    def __init__(self, pos, target_pos):
        Tank.__init__(self, pos, target_pos)
        # center the canon on the player by hand
        self.canon.update(pos, target_pos)
        self.time_trigger = 0
        self.time_counter = 0
        self.init_trigger()
        v = utils.get_volumes()[1]
        self.fire_sound.set_volume(v)

    def spot_player(self, path, target_pos, walls_group):
        # Raycasting principle : shoot a virtual bullet. If it ends up on a
        # wall, return False (the player is not on sight).
        # Else, it arrives on 'target_pos' and return True (the player is on
        # sight and a bullet can be shoot).
        fake_bullet = self.create_bullet(path, target_pos)
        test_rectangle = pygame.rect.Rect(0, 0, 30, 30)
        test_rectangle.center = target_pos
        while not test_rectangle.contains(fake_bullet.rect):
            fake_bullet.update(blit=False)
            if pygame.sprite.spritecollide(fake_bullet, walls_group, False,
                                           pygame.sprite.collide_rect):
                return False
        del fake_bullet
        return True

    def init_trigger(self):
        self.time_trigger = randint(100, 300)

    def generate_new_bullets(self, path, target_pos):
        """Generate only one bullet."""
        return self.create_bullet(path, target_pos)

    def update(self, path, target_pos, walls_group, pits_group,
               bullets_group, in_menu=False):
        new_bullets = None
        if not in_menu and self.alive:
            if self.time_counter > self.time_trigger and not in_menu:
                self.time_counter = 0
                self.init_trigger()
                if self.spot_player(path, target_pos, walls_group):
                    self.fire_sound.play()
                    new_generated_bullets = self.generate_new_bullets(
                        path, target_pos)
                    new_bullets = pygame.sprite.Group(new_generated_bullets)
                    self.bullets.add(new_generated_bullets)
            self.time_counter += 1
        Tank.update(self, path, target_pos, bullets_group)
        return new_bullets


class YellowPlusAI(YellowAI):
    """YellowPlusAI.

    A still AI that shoots the player on sight with 3 bullets at a time.
    """

    body_image_name = "tank_corps_yellowPlus.png"
    canon_image_name = "canon_yellowPlus.png"

    def generate_new_bullets(self, path, target_pos):
        """Generate three bullets.

        bullet_1 goes towards target_pos;
        bullet_2 a bit over it;
        bullet_3 a bit under it
        """
        delta = 12  # angular gap in degrees
        bullet_1 = self.create_bullet(path, target_pos)
        image_path = join(path, "images")
        x, y = bullet_1.rect.center
        bullet_2 = self.create_bullet(path, target_pos)
        bullet_2.__init__(image_path, x, y,
                          bullet_1.angle + math.radians(delta))
        bullet_3 = self.create_bullet(path, target_pos)
        bullet_3.__init__(image_path, x, y,
                          bullet_1.angle - math.radians(delta))
        return bullet_1, bullet_2, bullet_3


class BlueAI(YellowAI):
    """An AI that moves along a pre-defined path.

    Shoots the player on sight.
    """

    body_image_name = "tank_corps_blue.png"
    canon_image_name = "canon_blue.png"

    def __init__(self, pos, target_pos, points_list):
        YellowAI.__init__(self, pos, target_pos)
        self.points_list = points_list  # a list of tuples (x, y).
        # The AI will follow the list and go to the targets in
        # horizontal and vertical lines.
        self.step = 0  # the AI's step in its path.
        self.updater_class = YellowAI  # TODO change to super().update()

    def basic_move(self, path, target_pos):
        # moves the AI along its pre-defined path
        if self.points_list:
            self_x, self_y = self.body.rect.center
            goal_x, goal_y = self.points_list[self.step]
            v = self.body.speed
            if abs(self_x - goal_x) > v or abs(self_y - goal_y) > v:
                # we're still not at the goal point
                move_x, move_y = self.body.move_x, self.body.move_y
                self.body.stopvertical()  # always move on x first.
                if self_x < goal_x - v:
                    self.body.moveright()
                    self.body.goal_angle = 0
                elif self_x > goal_x + v:
                    self.body.moveleft()
                    self.body.goal_angle = 180
                else:
                    self.body.stophorizontal()
                    # on bouge ensuite en ordonnée
                    if self_y < goal_y - v:
                        self.body.movedown()
                        self.body.goal_angle = -90
                    elif self_y > goal_y + v:
                        self.body.moveup()
                        self.body.goal_angle = 90
            else:
                # we arrived at the goal point, go to the next.
                self.step += 1
                self.body.stop()
                if self.step == len(self.points_list):  # cycle the path.
                    self.step = 0

    def update(self, path, target_pos, walls_group, pits_group,
               bullets_group, in_menu=False):
        # deal with the path the AI must follow
        if not in_menu:
            self.basic_move(path, target_pos)
        # create the bullets and blit
        new_bullets = self.updater_class.update(
            self, path, target_pos, walls_group, pits_group,
            bullets_group, in_menu)
        return new_bullets


BluePlusAI = plussify(BlueAI)
BluePlusAI.canon_image_name = "canon_bluePlus.png"


class PurpleAI(BlueAI):
    """An AI that moves along a pre-defined path.

    Shoots the player on sight.
    A certain number of shots (3) are needed to kill it.
    """

    body_image_name = "tank_corps_purple.png"
    canon_image_name = "canon_purple.png"

    def __init__(self, pos, target_pos, points_list):
        BlueAI.__init__(self, pos, target_pos, points_list)
        self.max_shots = 3
        self.n_shots = 0
        chemin = path.replace("images", "music")
        v = utils.get_volumes()[1]
        self.destroyedSound = utils.load_sound("destroyed_sound.wav")
        self.destroyedSound.set_volume(v)
        self.fire_sound.set_volume(v)
        self.updater_class = YellowAI

    def update(self, path, target_pos, walls_group, pits_group, bullets_group,
               in_menu=False):
        if not in_menu:
            # deal with the path the AI must follow
            self.basic_move(path, target_pos)
            # test collisions with other bullets
            collided = pygame.sprite.spritecollide(self.body,
                                                   bullets_group, False)
            if collided:  # the AI was shot by a bullet
                for bullet in collided:
                    bullet.kill()
                self.destroyedSound.play()
                self.n_shots += 1
                if self.n_shots == self.max_shots:
                    self.alive = False
                else:
                    self.body.image = utils.load_image(
                        "tank_corps_purple_dmg{}.png"
                        .format(self.n_shots))[0]
                    self.body.base_image = self.body.image
        return self.updater_class.update(self, path, target_pos, walls_group,
                                         pits_group, bullets_group, in_menu)


PurplePlusAI = plussify(PurpleAI)
PurplePlusAI.canon_image_name = "canon_purplePlus.png"


class RedAI(YellowAI):
    """An AI that moves towards the player on a dynamically defined path.

    Shoots at the player on sight.
    """
    body_image_name = "tank_corps_red.png"
    canon_image_name = "canon_red.png"

    def __init__(self, pos, target_pos):
        YellowAI. __init__(self, pos, target_pos)
        self.points_list = []
        self.path_timer = 0
        self.path_timer_trigger = 200
        (x, y) = pos
        self.case = (x // 32, y // 32)
        self.updater_class = YellowAI  # TODO super().update()

    def get_new_path(self, target_pos, walls_group, pits_group):
        """A* algorithm.

        The Red AI finds the shortest path to get to the 'target_pos'
        position (generally the player's position).
        """
        # get initial and goal positions
        (x_target, y_target) = target_pos  # The target's position
        init_pos = self.case  # The initial position
        goal_pos = (x_target // 32, y_target // 32)  # The target's cell

        def get_default_dict(default_value):
            return {
                (i, j): default_value for i in range(32) for j in range(21)
            }

        # declare data containers
        obstacles = get_default_dict(True)
        seen = get_default_dict(False)
        # distance_matrix[i, j]:
        # shortest found distance from initial postion to (i, j)
        distance_matrix = get_default_dict(float("inf"))
        shortest_path = []
        # ^the shortest path to get to the target's position in terms of cells
        # parent_positions[i, j] : (i, j)'s neighbor on the shortest pass
        parent_positions = get_default_dict((-1, -1))
        queue_prio = PriorityQueue()

        # initialize data containers
        for wall in walls_group:  # Fill the matrix with walls ...
            obstacles[wall.pos] = False
        for pit in pits_group:  # ... and pits
            obstacles[pit.pos] = False
        distance_matrix[init_pos] = 0
        # ^Distance from start to start is obviously 0
        queue_prio.put((0, init_pos))

        # reach out for the goal position
        while not seen[goal_pos]:
            priority, x = queue_prio.get()
            if not seen[x]:
                for y in utils.get_neighbors(obstacles, x):
                    new_distance = (distance_matrix[x] +
                                    utils.heuristic(goal_pos, y))
                    if not seen[y] and new_distance < distance_matrix[y]:
                        queue_prio.put((new_distance, y))
                        distance_matrix[y] = new_distance
                        parent_positions[y] = x
                seen[x] = True

        # fallback to the initial position
        while goal_pos != init_pos:
            shortest_path.append(goal_pos)
            goal_pos = parent_positions[goal_pos]
        shortest_path = utils.clean(shortest_path)
        shortest_path.reverse()
        # ^shortest_path was (goal -> init) and we want (init -> goal)
        return [(32 * i + 16, 32 * j + 16) for i, j in shortest_path]

    def basic_move(self, path, target_pos):
        self_x, self_y = self.body.rect.center
        goal_x, goal_y = self.points_list[0]
        v = self.body.speed
        if abs(self_x - goal_x) > v or abs(self_y - goal_y) > v:
            # we're still not at the goal point
            move_x, move_y = self.body.move_x, self.body.move_y
            self.body.stopvertical()  # always move on x first.
            if self_x < goal_x - v:
                self.body.moveright()
                self.body.goal_angle = 0
            elif self_x > goal_x + v:
                self.body.moveleft()
                self.body.goal_angle = 180
            else:
                self.body.stophorizontal()  # on bouge ensuite en ordonnée
                if self_y < goal_y - v:
                    self.body.movedown()
                    self.body.goal_angle = -90
                elif self_y > goal_y + v:
                    self.body.moveup()
                    self.body.goal_angle = 90

        # on est arrivé au point. On se rend donc au point suivant
        else:
            self.body.stop()
            self.points_list.pop(0)  # on est arrivé, on enlève le point
        self.case = (self_x // 32, self_y // 32)
        self.path_timer += 1

    def update(self, path, target_pos, walls_group, pits_group, bullets_group,
               in_menu=False):
        if not in_menu:
            if not self.points_list:
                self.points_list = self.get_new_path(target_pos, walls_group,
                                                     pits_group)
            elif self.path_timer == self.path_timer_trigger:
                # time to compute a new path
                self.path_timer = 0
                self.points_list = self.get_new_path(target_pos, walls_group,
                                                     pits_group)
            self.basic_move(path, target_pos)
        return self.updater_class.update(self, path, target_pos, walls_group,
                                         pits_group, bullets_group, in_menu)


RedPlusAI = plussify(RedAI)
RedPlusAI.canon_image_name = "canon_redPlus.png"


class SpawnedAI(RedAI):
    """SpawnedAI : An AI that has been generated by a Spawner.

    Moves towards the player on a dynamically defined path.
    Shoots at the player on sight.
    """

    def __init__(self, pos, target_pos, spawner):
        RedAI.__init__(self, pos, target_pos)
        self.id = spawner  # the spawner which the AI belongs to


class SpawnedPlusAI(RedPlusAI):
    """SpawnedPlusAI : An AI that has been generated by a Spawner.

    Moves towards the player on a dynamically defined path.
    Shoots at the player on sight 3 bullets at a time.
    """

    def __init__(self, pos, target_pos, spawner):
        RedPlusAI.__init__(self, pos, target_pos)
        self.id = spawner  # the spawner which the AI belongs to


class Spawner(pygame.sprite.Sprite):
    """Spawner : An AI that generates RedAI's.

    A single shot is enough to kill it.
    """

    def __init__(self, sprite_name, pos,
                 spawned_body_name="tank_corps_spawned.png",
                 spawned_canon_name="canon_spawned.png"):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = utils.load_image(sprite_name)
        self.base_image = self.image
        self.area = pygame.display.get_surface().get_rect()
        self.rect.center = pos
        self.spawned_body_name = spawned_body_name
        self.spawned_canon_name = spawned_canon_name
        self.max_shots = 1
        self.n_shots = 0
        self.time_counter = 300
        self.time_trigger = 0
        self.alive = True
        self.spawned = False
        # ^True if an AI spawned by this spawner is still alive
        self.destroyedSound = utils.load_sound("destroyed_sound.wav")
        self.destroyedSound.set_volume(utils.get_volumes()[1])
        self.init_trigger()

    def init_trigger(self):
        self.time_trigger = randint(100, 300)

    def update(self, path, target_pos, bullets_group):
        if self.alive:
            generated_AI = None
            if not self.spawned:
                if self.time_counter >= self.time_trigger:
                    self.time_counter = 0
                    self.init_trigger()
                    self.spawned = True
                    pos = self.rect.center
                    image_path = join(path, "images")
                    generated_AI = SpawnedAI(
                        image_path, self.spawned_body_name,
                        self.spawned_canon_name, pos,
                        target_pos, self)
                else:
                    self.time_counter += 1
            collided = pygame.sprite.spritecollide(self, bullets_group, False)
            if collided:
                self.destroyedSound.play()
                for bullet in collided:
                    bullet.kill()
                self.n_shots += 1
                if self.n_shots == self.max_shots:
                    self.alive = False
                else:
                    self.image = utils.load_image("spawner_dmg{}.png"
                                                  .format(self.n_shots))[0]
        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)
        return generated_AI


class SpawnerPlus(Spawner):
    """SpawnerPlus : An AI that generates RedPlusAI's.

    3 shots are needed to kill it.
    """

    def __init__(self, path, sprite_name, pos,
                 spawned_body_name="tank_corps_spawned.png",
                 spawned_canon_name="canon_spawnedPlus.png"):
        Spawner.__init__(self, path, sprite_name, pos, spawned_body_name,
                         spawned_canon_name)
        self.max_shots = 3


class IATurret:  # TODO
    """TurretAI.

    An AI that shoots bullets in all directions at regular intervals.
    """

    def __init__(self, path, sprite_name, pos, target_pos):
        pass
