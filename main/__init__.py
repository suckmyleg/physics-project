from main.phisics import *
from main.visuals import *
from main.debug import *
import time
import copy

class Simulation:
	def debug(self, function_name, args=False, sep=False, error=False):
		self.Debug.debug("Simulation", function_name, args, sep=sep, error=error)

	def main(self):
		for i in range(10000):
			if not self.pause:
				actions = self.visuals.reload(self.phisics.objects)
			else:
				actions = self.visuals.reload(self.phisics.objects)
			self.handle_events(actions)
			self.debug("main", sep="Reload")


	def setup(self):
		self.debug("setup")

	def load(self, lvl):
		self.debug("load", args=[lvl])
		e = [{"visual":{"layer":1,"color":[150,1,1],"visible":True,"body":[{"A":[1,1],"B":[20,20],"color":False}]},"collider":{"mass":1,"static":True,"body":[{"A":[1,1],"B":[1,1],"AB":[1,1]}]}}]
		for i in range(2):
			e[0]["visual"]["layer"] += i
			self.phisics.add_objects(e)

	def start(self):
		self.debug("start")
		self.main()

	#DEBUG CONTROLLS

	def debug_zoom_in(self):
		self.debug("debug_zoom_in")
		self.visuals.change_font_size(self.visuals.font_size + 1)

	def debug_zoom_out(self):
		self.debug("debug_zoom_out")
		self.visuals.change_font_size(self.visuals.font_size - 1)

	def debug_down(self):
		self.debug("debug_down")
		self.visuals.font_default_height -= 1

	def debug_up(self):
		self.debug("debug_up")
		self.visuals.font_default_height += 1

	def switch_debug(self):
		self.debug("switch_debug")
		if self.visuals.show_debug:
			self.visuals.show_debug = False
		else:
			self.visuals.show_debug = True

	def switch_pause(self):
		self.debug("handle_events")
		if self.pause:
			self.pause = False
		else:
			self.pause = True


	#PLAYER CONTROLLS

	def player_move_forward(self):
		if not self.pause:
			self.debug("player_move_forward")
			self.phisics.move_object(self.phisics.objects[0], 0, -1)

	def player_move_back(self):
		if not self.pause:
			self.debug("player_move_back")
			self.phisics.move_object(self.phisics.objects[0], 0, 1)

	def player_move_left(self):
		if not self.pause:
			self.debug("player_move_left")
			self.phisics.move_object(self.phisics.objects[0], -1, 0)

	def player_move_right(self):
		if not self.pause:
			self.debug("player_move_right")
			self.phisics.move_object(self.phisics.objects[0], 1, 0)


	def handle_events(self, events):
		self.debug("handle_events")
		for e in events:
			for c in self.controlls:
				if c[0] == e.type or c[0] == "k_hold":
					if c[0] == self.types["scroll"]:
						key = e.button
					else:
						try:
							key = e.key
						except:
							if c[0] == "k_hold":
								key = e

					if key == c[1]:
						c[2]()
						break


	def uknown_command(self):
		self.debug("uknown_command")

	def setup_key(self, k):
		key = k[1]

		try:
			key = self.keys[k[1]]
		except:
			pass

		try:
			function = self.commands[k[2]]
			if not function:
				function = self.uknown_command
				self.debug("setup_key", error="Uknwon command: {}".format(k[2]))
		except:
			function = self.uknown_command
			self.debug("setup_key", error="Uknwon command: {}".format(k[2]))
		else:
			self.debug("setup_key")

		return [self.types[k[0]], key, function]

	def setup_controlls(self, keys_map):
		self.debug("setup_controlls")

		for k in keys_map:
			self.controlls.append(self.setup_key(k))


	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", debug_interval_time=1, fps=60, keys_map=False, output_console=True):
		self.Debug = Debug(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, interval_time=debug_interval_time, output_console=output_console)
		self.debug("__init__", sep="Start")

		self.phisics = PHISICS(debug=self.Debug.debug)
		self.visuals = VISUALS(debug=self.Debug, fps=fps)

		self.pause = False

		self.debug_mode = False

		self.keys_map = keys_map
		
		self.types = {"scroll":pygame.MOUSEBUTTONDOWN, "k_down":pygame.KEYDOWN, "k_up":pygame.KEYUP, "k_hold":"k_hold"}

		self.keys = {"k_down":pygame.K_DOWN, "k_up":pygame.K_UP, "k_space":pygame.K_SPACE, "k_rshift":pygame.K_RSHIFT, "k_escape":pygame.K_ESCAPE, "k_a":pygame.K_a, "k_s":pygame.K_s, "k_d":pygame.K_d, "k_w":pygame.K_w}

		self.commands = {"player_move_forward":self.player_move_forward, "player_move_back":self.player_move_back, "player_move_left":self.player_move_left, "player_move_right":self.player_move_right, "switch_pause":self.switch_pause, "zoom_in":self.debug_zoom_in, "zoom_out":self.debug_zoom_out, "debug_down":self.debug_down, "debug_up":self.debug_up, "switch_debug":self.switch_debug}
		
		self.controlls = []

		self.setup_controlls(self.keys_map)










