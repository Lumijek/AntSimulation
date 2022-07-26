import pygame
import random


class Food:
    def __init__(self, x, y, attractiveness, color, idg):
        self.x = x
        self.y = y
        self.attractiveness = attractiveness
        self.img = pygame.Surface((6, 6))
        pygame.draw.circle(self.img, color, (3, 3), 3)
        self.img.set_colorkey("BLACK")
        self.taken = False
        self.ant = None

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def get_attractiveness(self):
        return self.attractiveness

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def move(self, x, y):
        self.x = x
        self.y = y
