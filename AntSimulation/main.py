import math
import pygame
import sys
from ants import ant
import random
import food
from pointquadtree import PointQuadTree
import time
from pheremones.pheremone import Pheremone

pygame.init()
WIDTH, HEIGHT = (1280, 800)

class AntSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill("BLACK")
        pygame.display.set_caption("Ant Simulation")
        self.foodquadtree = PointQuadTree(0, 0, WIDTH, HEIGHT, 10, 5)
        self.home_pqt = PointQuadTree(0, 0, WIDTH, HEIGHT, 10, 5)
        self.food_pqt = PointQuadTree(0, 0, WIDTH, HEIGHT, 10, 5)

    def run(self):
        ant_list = []
        food_list = []
        home_pheremones = []
        food_pheremones = []

        for i in range(1000):
            ant_list.append(
                ant.Ant(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
            )

        for i in range(1000):
            new_food = food.Food(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.randint(1, 1000),
                "GREEN",
                i,
            )
            food_list.append(new_food)
            self.foodquadtree.insert(new_food)
        clock = pygame.time.Clock()
        prev_time = time.perf_counter()
        while True:
            self.screen.fill("BLACK")
            dt = time.perf_counter() - prev_time
            prev_time = time.perf_counter()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for foods in food_list:
                foods.draw(self.screen)

            for ph in home_pheremones:
                ph.update_pheremone(dt)
                ph.draw(self.screen)
                if ph.intensity < 0.05:
                    home_pheremones.remove(ph)
                    self.home_pqt.remove(ph)
            for ph in food_pheremones:
                ph.update_pheremone(dt)
                ph.draw(self.screen)
                if ph.intensity < 0.05:
                    food_pheremones.remove(ph)
                    self.food_pqt.remove(ph)

            for ants in ant_list:
                ants.draw(self.screen, dt)
                ants.handle_food(food_list, self.foodquadtree)
                if ants.draw_pher:
                    if not ants.has_food:
                        pheremone1 = Pheremone(ants.x, ants.y, 1, 0)
                        home_pheremones.append(pheremone1)
                        self.home_pqt.insert(pheremone1)
                    else:
                        pheremone2 = Pheremone(ants.x, ants.y, 1, 1)
                        food_pheremones.append(pheremone2)
                        self.food_pqt.insert(pheremone2)

                    ants.draw_pher = False


                #pygame.draw.circle(self.screen, "GREEN", (ants.x + distance * math.cos(angle + math.radians(50)), ants.y + distance * math.sin(angle + math.radians(50))), 20)
                #pygame.draw.circle(self.screen, "GREEN", (ants.x + distance * math.cos(angle), ants.y + distance * math.sin(angle)), 20)
                #pygame.draw.circle(self.screen, "GREEN", (ants.x + distance * math.cos(angle - math.radians(50)), ants.y + distance * math.sin(angle - math.radians(50))), 20)
                ### FOR RECTANGLES
                #angle = ants.angle
                #distance = 50
                #pygame.draw.rect(self.screen, "GREEN", (ants.x + distance * math.cos(angle + math.radians(40)) - 10, ants.y + distance * math.sin(angle + math.radians(40)) - 10, 40, 40))
                #pygame.draw.rect(self.screen, "GREEN", (ants.x + distance * math.cos(angle) - 10, ants.y + distance * math.sin(angle) - 10, 40, 40))
                #pygame.draw.rect(self.screen, "GREEN", (ants.x + distance * math.cos(angle - math.radians(40)) - 10, ants.y + distance * math.sin(angle - math.radians(40)) - 10, 40, 40))
            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    sim = AntSimulation()
    sim.run()
