import pygame
import time

class Pheremone:
	def __init__(self, x, y, intensity, state):
		self.x = x
		self.y = y
		self.intensity = intensity
		self.state = state # 0 is home pheremone and 1 is food pheremone. Maybe will add "stay-away" pheremone later
		if self.state == 0:
			self.color = "RED"
		elif self.state == 1:
			self.color = "BLUE"
		self.img = pygame.Surface((8, 8))
		pygame.draw.circle(self.img, self.color, (4, 4), 4)
		self.img.set_colorkey("Black")
		self.total_time = 0
		self.max_time = 15

	def draw(self, screen):
		screen.blit(self.img, (self.x - 3, self.y - 3))

	def update_pheremone(self, dt):
		self.total_time += dt
		self.intensity = 1 - self.total_time / self.max_time
		evap_amount = 170 * self.intensity
		self.img.set_alpha(evap_amount)






