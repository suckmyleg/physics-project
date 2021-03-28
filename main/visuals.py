from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import copy
import pygame
from time import sleep

class VISUALS:
	def debug(self, function_name, args=False, sep=False):
		if self.debug_c:
			self.debug_c.debug("VISUALS", function_name, args=args, sep=sep)

	def main(self):
		self.debug("main")

	def draw_line(self, l, color):
		self.debug("draw_line")
		if l["color"]:
			color = color

		if self.show_debug:
			self.show_message("Ax: {} - Ay: {} - Bx: {} - By: {} {}".format(l["A"][0], l["A"][1], l["B"][0], l["B"][1], color))

		pygame.draw.line(self.screen, color, l["A"], l["B"])


	def draw_object(self, o):
		self.debug("draw_object")
		visual = o["visual"]
		color = visual["color"]

		for l in visual["body"]:
			self.draw_line(l, color)

	def get_highest_layer(self, objects):
		self.debug("get_highest_layer", args=len(objects))
		highest = False
		i = -1
		for o in objects:
			i += 1
			if not highest or highest["visual"]["layer"] < o["visual"]["layer"]:
				highest = o
		del objects[i]
		return highest, objects

	def order_objects_by_layers(self, objects):
		self.debug("order_objects_by_layers", args=len(objects))
		ordered = []
		for i in range(len(objects)):
			high, objects = self.get_highest_layer(objects)
			ordered.append(high)

		return ordered

	def show_messages(self, messages):
		self.debug("show_messages")
		for m in messages:
			self.show_message(m)

	def show_message(self, message, deb=True):
		if deb:
			self.debug("show_message")
		message = str(message)
		label = self.myFont.render(message, True, (0,128,255))
		self.screen.blit(label, (10, self.message_n*self.font_size + self.font_default_height))
		self.message_n += 1

	def info(self):
		self.debug("info")
		if self.show_debug:
			self.mouse_info()
			self.screen_info()
			self.debug_info()

	def debug_info(self):
		self.debug("debug_info")
		messages = copy.deepcopy(self.debug_c.messages)
		messages[0] = ""
		self.show_messages(messages)

	def mouse_info(self):
		self.debug("mouse_info")
		x,y = pygame.mouse.get_pos()
		self.show_message("mouse coords: {}, {}".format(str(x), str(y)))

	def screen_info(self):
		self.debug("screen_info")
		self.show_message("screen: {}x{}".format(self.width, self.height))
		self.show_message("fps: {}".format(self.fps))
		self.show_message("debug_size: {}".format(self.font_size))
		self.show_message("debug_mode: {}".format(self.debug_c.debug_mode))

	def update_screen(self):
		self.debug("update_screen")
		self.message_n = 0.1
		pygame.display.flip()

	def clear_screen(self):
		self.debug("clear_screen")
		self.screen.fill((0,0,0))

	def reload(self, objects=False):
		self.debug("reload")
		actions = self.get_actions()
		self.clear_screen()
		self.info()
		if objects:
			self.draw_objects(objects)
		self.update_screen()
		self.fpsClock.tick(self.fps)
		return actions

	def get_actions(self):
		self.debug("get_actions")
		return pygame.event.get()

	def draw_objects(self, phisics_objects):
		objects = copy.deepcopy(phisics_objects)
		self.debug("draw_objects", args=len(objects))

		self.show_message("")

		for o in self.order_objects_by_layers(objects):
			self.draw_object(o)

	def change_font_size(self, font_size):
		self.debug("change_font_size")
		if font_size < 8:
			font_size = 8
		else:
			if font_size > 33:
				font_size = 33
		self.font_size = font_size
		self.myFont = pygame.font.SysFont('arial', self.font_size, True, False)

	def __init__(self, width=1920, height=1080, debug=False, fps=60, show_debug=False):
		self.show_debug = show_debug
		self.debug_c = debug
		self.debug("__init__")
		self.width = width
		self.height = height
		self.fps = fps
		self.fpsClock = pygame.time.Clock()
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.change_font_size(11)
		self.font_default_height = 10
		self.message_n = 0.1