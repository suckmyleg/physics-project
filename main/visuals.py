from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import copy
import pygame
from time import sleep
from threading import Thread

class VISUALS:
	def draw_rect(self, o):
		self.debug("draw_rect")

		pygame.draw.rect(self.screen, o.color, pygame.Rect(o.x, o.y, o.height, o.width))

	def draw_actual_speed(self, o):
		self.debug("draw_actual_speed")
		color = (0, 250, 0)

		default = - 0.5

		if self.show_speed_labels:

			labelx = self.myFont.render("sx: {}*10^(-2) m/s".format(int(o.speed.x*100)), True, (0,128,255))
			self.screen.blit(labelx, (o.x, -3*self.font_size + o.y + default))

			labely = self.myFont.render("sy: {}*10^(-2) m/s".format(int(o.speed.y*100)), True, (0,128,255))
			self.screen.blit(labely, (o.x, -2*self.font_size + o.y + default))

			labeln = self.myFont.render("masa: {}kg".format(int(o.mass*10)), True, (0,128,255))
			self.screen.blit(labeln, (o.x, -1*self.font_size + o.y + default))



		#pygame.draw.line(self.screen, color, o.center_vector, [o.center_vector[0] + o.speed.x*1, o.center_vector[1]])
		#pygame.draw.line(self.screen, color, o.center_vector, [o.center_vector[0], o.center_vector[1]+o.speed.y*1])

		
		if self.show_speed_gravity_direction:

			for i in o.speed.interactions:
			
				pygame.draw.line(self.screen, color, o.center_vector, [o.center_vector[0] + i[0]*1000, o.center_vector[1] + i[1]*1000])
		

	def draw_object(self, o):
		self.debug("draw_object")
			
		self.draw_rect(o)

		if self.show_objects_speeds:
			self.draw_actual_speed(o)

	def get_highest_layer(self, objects):
		self.debug("get_highest_layer", args=len(objects))
		highest = False
		i = -1
		for o in objects:
			i += 1
			if not highest or highest.layer < o.layer:
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

	def info(self, show=False):
		self.debug("info")
		if self.show_debug or show:
			self.mouse_info()
			self.screen_info()
			self.phisics_info()
			self.debug_info()
			self.debug_errors()

	def show_messages_folder(self, title, messages, fun=False):
		self.debug("show_messages_folder")
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

	def phisics_info(self):
		self.debug("screen_info")
		messages = [
		"scale: {}".format(self.phisics.distance_scale),
		"n_objects: {}".format(len(self.phisics.objects))
		]
		self.show_messages_folder("Phisics", messages)

	def screen_info(self):
		self.debug("screen_info")
		messages = ["resolution: {}x{}".format(self.width, self.height), 
		"fps: {}".format(int(self.current_fps)), 
		"debug_size: {}".format(self.font_size), 
		"debug_mode: {}".format(self.debug_c.debug_mode)]
		self.show_messages_folder("Screen", messages)


	def update_screen(self):
		self.debug("update_screen")
		self.message_n = 0.1
		self.clock.tick()
		self.current_fps = self.clock.get_fps()
		pygame.display.flip()

	def clear_screen(self, color=(0,0,0)):
		self.debug("clear_screen")
		self.screen.fill(color)

	def reload(self, objects=False, fps=False):
		self.debug("reload")
		if not fps:
			fps = self.fps
		actions = self.get_actions()
		self.clear_screen()
		if objects:
			self.draw_objects(objects)
		self.info()
		self.update_screen()
		self.clock.tick(fps)
		return actions

	def get_actions(self):
		self.debug("get_actions")
		return pygame.event.get()

	def remove_out(self, objects):
		self.debug("remove_out")
		
		for o in objects:
			if o.x > self.width or o.x < 0:
				o.remove()
			else:
				if o.y > self.height or o.y < 0:
					o.remove()

	def draw_objects(self, phisics_objects):
		try:
			self.remove_out(phisics_objects)
			self.debug("draw_objects")

			for o in phisics_objects:
				self.draw_object(o)
		except Exception as e:
			self.debug("draw_objects", error=e)

	def change_font_size(self, font_size):
		self.debug("change_font_size")
		if font_size < 8:
			font_size = 8
		else:
			if font_size > 33:
				font_size = 33
		self.font_size = font_size
		self.myFont = pygame.font.SysFont('monospace', self.font_size, True, False)












	def __init__(self, phisics, width=1080, height=720, debug=False, fps=60, show_debug=False):
		self.phisics = phisics
		self.show_debug = show_debug
		self.debug_c = debug
		self.debug = self.debug_c.get_debug("VISUALS")
		self.debug("__init__")
		self.width = width
		self.height = height
		self.fps = fps
		self.current_fps = fps
		self.show_objects_speeds = False
		self.show_speed_labels = False
		self.show_speed_gravity_direction = True
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.pygame = pygame
		self.clock = self.pygame.time.Clock()
		self.change_font_size(11)
		self.font_default_height = 10
		self.message_n = 0.1