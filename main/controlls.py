class CONTROLLS:
	#DEBUG CONTROLLS

	def debug_zoom_in(self):
		self.debug("debug_zoom_in")
		self.visuals.change_font_size(self.visuals.font_size + 1)

	def debug_zoom_out(self):
		self.debug("debug_zoom_out")
		self.visuals.change_font_size(self.visuals.font_size - 1)

	def debug_up(self):
		self.debug("debug_up")
		self.visuals.font_default_height -= 1

	def debug_down(self):
		self.debug("debug_down")
		self.visuals.font_default_height += 1

	def switch_debug(self):
		self.debug("switch_debug")
		if self.visuals.show_debug:
			self.visuals.show_debug = False
		else:
			self.visuals.show_debug = True

	def switch_pause(self):
		self.debug("switch_pause")
		if self.pause:
			self.pause = False
		else:
			self.pause = True


	#PLAYER CONTROLLS

	def object_move_forward(self, object_id=0):
		if not self.pause:
			self.debug("object_move_forward")
			self.phisics.move_rect(self.phisics.objects[object_id], 0, -5)

	def object_move_back(self, object_id=0):
		if not self.pause:
			self.debug("object_move_back")
			self.phisics.move_rect(self.phisics.objects[object_id], 0, 5)

	def object_move_left(self, object_id=0):
		if not self.pause:
			self.debug("object_move_left")
			self.phisics.move_rect(self.phisics.objects[object_id], -5, 0)

	def object_move_right(self, object_id=0):
		if not self.pause:
			self.debug("object_move_right")
			self.phisics.move_rect(self.phisics.objects[object_id], 5, 0)

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



	def __init__(self, keys_map, pygame, debug, debug_mode, main):
		self.debug = debug.get_debug("CONTROLLS", debug_mode)
		self.debug("__init__")

		self.main = main

		self.phisics = self.main.phisics

		self.visuals = self.main.visuals

		self.keys_map = keys_map
		
		self.types = {"scroll":pygame.MOUSEBUTTONDOWN, "k_down":pygame.KEYDOWN, "k_up":pygame.KEYUP, "k_hold":"k_hold"}

		self.keys = {"k_down":pygame.K_DOWN, "k_up":pygame.K_UP, "k_space":pygame.K_SPACE, "k_rshift":pygame.K_RSHIFT, "k_escape":pygame.K_ESCAPE, "k_a":pygame.K_a, "k_s":pygame.K_s, "k_d":pygame.K_d, "k_w":pygame.K_w}

		self.commands = {"object_move_forward":self.object_move_forward, "object_move_back":self.object_move_back, "object_move_left":self.object_move_left, "object_move_right":self.object_move_right, "switch_pause":self.switch_pause, "zoom_in":self.debug_zoom_in, "zoom_out":self.debug_zoom_out, "debug_down":self.debug_down, "debug_up":self.debug_up, "switch_debug":self.switch_debug}
		
		self.controlls = []

		self.actions = []

		self.pause = False