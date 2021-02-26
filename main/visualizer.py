import pygame

class Graphic:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1280,720))

	def print_line(self, l):
		pygame.draw.line(self.screen, (255, 0, 0), [l[0][0], l[0][1]], [l[1][0], l[1][1]])

	def print_object(self, o):
		for l in o:
			self.print_line(l)
			pygame.display.update()

	def show_objects(self, objects):
		self.screen.fill((0,0,0))
		for o in objects:
			self.print_object(o)
		pygame.display.flip()
		pygame.display.update()