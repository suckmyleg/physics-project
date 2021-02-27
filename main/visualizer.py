import pygame
from random import randint as ra

class Graphic:
	def __init__(self, width=1280, height=720):
		self.width = width
		self.height = height
		self.objects = []

	def start_display(self):
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))

	def print_line(self, l, color=False):
		if not color:
			color = (255, 0, 0)
		pygame.draw.line(self.screen, color, [l[0][0], l[0][1]], [l[1][0], l[1][1]])

	def print_object(self, o, color=False):
		for l in o:
			self.print_line(l, color=color)
			pygame.display.update()

	def get_position_click(self, start_point=False):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					return pygame.mouse.get_pos()
				else:
					if start_point:
						self.show_objects([[[start_point, pygame.mouse.get_pos()]]])


	def make_rect(self):
		A = self.get_position_click()
		return [A, self.get_position_click(A)]


	def show_objects(self, objects=[], color=False):
		self.screen.fill((0,0,0))
		for o in objects + self.objects:
			self.print_object(o, color=color)
		pygame.display.flip()
		pygame.display.update()