import pygame
import math
import sys
import random
from pheremones.pheremone import Pheremone
from pointquadtree import PointQuadTree


def euclid_distance_no_sqrt(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

class Ant:
    def __init__(self, x, y, width, height):
        self.img = pygame.image.load("images/ant.png").convert_alpha()
        self.img = pygame.transform.smoothscale(
            self.img, (self.img.get_width() * 0.15, self.img.get_height() * 0.15)
        )
        self.img = pygame.transform.rotate(self.img, -90)
        self.original_image = self.img
        self.rect = self.img.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.velocity = 100
        self.angle = random.randint(0, 360)
        self.img = pygame.transform.rotate(
            self.original_image, -math.degrees(self.angle)
        )
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.collist = [-15, -30, -45, 15, 30, 45]
        self.has_food = False
        self.food_target = None
        self.bounds = (width, height)
        self.angletime = 0
        self.time_to_update_angle = 0.07
        self.pher_time = 0
        self.time_to_add_pher = 0.2
        self.draw_pher = False

    def turn(self):

        if self.food_target != None and self.has_food == False:
            diff_x = self.food_target.get_x() - self.x
            diff_y = self.food_target.get_y() - self.y
            self.angle = math.atan2(diff_y, diff_x)
            self.img = pygame.transform.rotate(
                self.original_image, -math.degrees(self.angle)
            )
            self.rect = self.img.get_rect(center=(self.x, self.y))

        else:
            if self.angletime >= self.time_to_update_angle:
                self.angle += math.radians(random.randint(-10, 10))
                self.angletime = 0
            else:
                self.img = pygame.transform.rotate(
                    self.original_image, -math.degrees(self.angle)
                )
                self.rect = self.img.get_rect(center=(self.x, self.y))

    def move(self, angle, dt):
        """
        Moves ant in direction specified
        """
        self.x += math.cos(angle) * self.velocity * dt
        self.y += math.sin(angle) * self.velocity * dt

        if self.pher_time >= self.time_to_add_pher:
            self.pher_time = 0
            self.draw_pher = True

            self.pher_time = 0
        if self.x >= self.bounds[0] or self.x <= 0:
            self.x -= math.cos(angle) * self.velocity * dt
            self.angle += math.radians(random.choice(self.collist))
        if self.y >= self.bounds[1] or self.y <= 0:
            self.y -= math.sin(angle) * self.velocity * dt
            self.angle += math.radians(random.choice(self.collist))

    def find_nearby_food(self, quadtree):
        b = quadtree.query_circle2((self.x, self.y), 30)
        return b

    def handle_food(self, food_list, quadtree):
        if self.has_food == False:
            if self.food_target == None:
                nearby_foods = self.find_nearby_food(quadtree)
                if len(nearby_foods) == 0:
                    return
                nearby_foods.sort(
                    key=lambda food: food.get_attractiveness(), reverse=True
                )
                for target_food in nearby_foods:
                    if target_food.taken == False:
                        self.food_target = target_food
                        target_food.taken = True
                        target_food.ant = self
                        break

            else:
                if euclid_distance_no_sqrt(
                    self.x, self.y, self.food_target.get_x(), self.food_target.get_y()
                ) < pow(2, 4):
                    self.has_food = True

        if self.has_food:
            self.food_target.move(self.x, self.y)

    def draw(self, screen, dt):
        self.angletime += dt
        self.pher_time += dt
        #print(self.pher_time)

        self.turn()
        self.move(self.angle, dt)

        screen.blit(self.img, self.rect)