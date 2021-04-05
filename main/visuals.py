from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import copy
import pygame
from time import sleep

class VISUALS:
	def draw_rect(self, l, color):
		self.debug("draw_rect")
		if l["color"]:
			color = color

		if self.show_debug:
			self.show_message("l: {}".format(l))

		pygame.draw.rect(self.screen, color, pygame.Rect(l["x"], l["y"], l["h"], l["w"]))

	def draw_line(self, l, color):
		self.debug("draw_line")
		if l["color"]:
			color = color

		if self.show_debug:
			self.show_message("Ax: {} - Ay: {} - Bx: {} - By: {} {}".format(l["A"][0], l["A"][1], l["B"][0], l["B"][1], color))

		pygame.draw.line(self.screen, color, l["A"], l["B"])


	def draw_actual_speed(self, x, y, x0, y0, ix, iy, m, w, h):
		self.debug("draw_actual_speed")
		color = (0, 250, 0)

		default = - 0.5

		labelx = self.myFont.render("sx: {}*10^(-2) m/s".format(int(x*100)), True, (0,128,255))
		self.screen.blit(labelx, (ix, -3*self.font_size + iy + default))

		labely = self.myFont.render("sy: {}*10^(-2) m/s".format(int(y*100)), True, (0,128,255))
		self.screen.blit(labely, (ix, -2*self.font_size + iy + default))

		labeln = self.myFont.render("masa: {}kg".format(int(m*10)), True, (0,128,255))
		self.screen.blit(labeln, (ix, -1*self.font_size + iy + default))



		pygame.draw.line(self.screen, color, [x0, y0], [x0+x*10, y0])
		pygame.draw.line(self.screen, color, [x0, y0], [x0, y0+y*10])

	def draw_object(self, o):
		self.debug("draw_object")
		visual = o["visual"]

		if visual["visible"]:
			color = visual["color"]
			
			self.draw_rect(visual["body"], color)

			self.draw_actual_speed(o["collider"]["movement"]["x"], o["collider"]["movement"]["y"], o["collider"]["body"]["vectors"][4][0], o["collider"]["body"]["vectors"][4][1], o["collider"]["body"]["x"], o["collider"]["body"]["y"], o["collider"]["mass"], o["collider"]["body"]["w"], o["collider"]["body"]["h"])

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
		label = self.myFont.render(str(message), True, (0,128,255))
		self.screen.blit(label, (10, self.message_n*self.font_size + self.font_default_height))
		self.message_n += 1

	def info(self):
		self.debug("info")
		if self.show_debug:
			self.mouse_info()
			self.screen_info()
			self.debug_info()
			self.debug_errors()

	def show_messages_folder(self, title, messages, fun=False):
		if not fun:
			fun = self.show_messages

		self.show_message("")
		self.show_message("{}:".format(title))
		fun(messages)


	def show_errors(self, errors):
		self.debug("show_errors")
		for m in errors:
			m = "[{}.{}()] [{}][{}] Exception => {}".format(m[0], m[1], m[4], m[3], m[2])
			self.show_message(m)

	def debug_errors(self):
		self.debug("debug_errors")
		messages = copy.deepcopy(self.debug_c.errors)
		self.show_messages_folder("Errors", messages, fun=self.show_errors)

	def debug_info(self):
		self.debug("debug_info")
		messages = copy.deepcopy(self.debug_c.messages)
		if len(messages) > 0 and True:
			del messages[0]
		self.show_messages_folder("Calls", messages)

	def get_mouse_pos(self):
		return pygame.mouse.get_pos()

	def mouse_info(self):
		self.debug("mouse_info")
		x, y = self.get_mouse_pos()
		messages = ["mouse coords: {}, {}".format(str(x), str(y))]
		self.show_messages_folder("Input", messages)

	def screen_info(self):
		self.debug("screen_info")
		messages = ["resolution: {}x{}".format(self.width, self.height), 
		"fps: {}".format(self.fps), 
		"debug_size: {}".format(self.font_size), 
		"debug_mode: {}".format(self.debug_c.debug_mode)]
		self.show_messages_folder("Screen", messages)


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
		if objects:
			self.draw_objects(objects)
		self.info()
		self.update_screen()
		self.fpsClock.tick(self.fps)
		return actions

	def get_actions(self):
		self.debug("get_actions")
		return pygame.event.get()

	def remove_out(self, objects):
		
		for o in objects:
			if o["collider"]["body"]["x"] > self.width or o["collider"]["body"]["x"] < 0:
				del objects[objects.index(o)]
			else:
				if o["collider"]["body"]["y"] > self.height or o["collider"]["body"]["y"] < 0:
					del objects[objects.index(o)]

	def draw_objects(self, phisics_objects):
		try:
			self.remove_out(phisics_objects)
			objects = copy.deepcopy(phisics_objects)
			self.debug("draw_objects")

			self.show_message("")

			for o in objects:#self.order_objects_by_layers(objects):
				self.draw_object(o)
		except Exception as e:
			self.debug("draw_object", error=e)

	def change_font_size(self, font_size):
		self.debug("change_font_size")
		if font_size < 8:
			font_size = 8
		else:
			if font_size > 33:
				font_size = 33
		self.font_size = font_size
		self.myFont = pygame.font.SysFont('monospace', self.font_size, True, False)

	def __init__(self, width=1080, height=720, debug=False, debug_mode=5, fps=60, show_debug=False):
		self.show_debug = show_debug
		self.debug_c = debug
		self.debug = self.debug_c.get_debug("VISUALS", debug_mode)
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