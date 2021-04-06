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
			self.phisics.pause = False
		else:
			self.phisics.pause = True
			self.pause = True

	def reload_lvl(self):
		self.debug("reload_lvl")
		self.main.reload_lvl()

	def change_lvl(self):
		self.main.load_lvl(6)


	#PLAYER CONTROLLS

	def object_move_forward(self, object_id=0):
		if not self.pause:
			self.debug("object_move_forward")
			self.phisics.push_rect(self.phisics.objects[object_id], 0, -1)

	def object_move_back(self, object_id=0):
		if not self.pause:
			self.debug("object_move_back")
			self.phisics.push_rect(self.phisics.objects[object_id], 0, 1)

	def object_move_left(self, object_id=0):
		if not self.pause:
			self.debug("object_move_left")
			self.phisics.push_rect(self.phisics.objects[object_id], -1, 0)

	def object_move_right(self, object_id=0):
		if not self.pause:
			self.debug("object_move_right")
			self.phisics.push_rect(self.phisics.objects[object_id], 1, 0)

	def spawn_new_rect(self, x, y, mass=100000000000, color=[150,1,250]):
		rect = {
    "visual": {
      "layer": 1,
      "color": color,
      "visible": True,
      "body": {
        "x": x,
        "y": y,
        "h": 10,
        "w": 10,
        "color": False
      }
    },
    "collider": {
      "mass": mass,
      "static": False,
      "body": {
        "x": x,
        "y": y,
        "w": 10,
        "h": 10
      }
    }
  }
		self.phisics.add_objects([rect])

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
			data = self.setup_key(k)
			self.controlls[str(data[1])] = {"type":data[0], "function":data[2]}


	def get_function_from_command(self, command):
		return self.commands[command]

	def execute_command(self, command):
		self.get_function_from_command(command)()

	def active_command(self, command):
		if not command in self.active_commands:
			self.active_commands.append(command)

	def inactive_command(self, command):
		if command in self.active_commands:
			del self.active_commands[self.active_commands.index(command)]

	def get_type_of_event(self, event):
		for t in self.types.keys():
			if event.type in self.types[t]:
				return t

	def get_value_from_event(self, e, event_type):
		if event_type == "scroll" or event_type == "click":
			return e.button
		else:
			if event_type in ["k_down", "k_up"]:
				return e.key
			else:
				return False

	def handle_events(self, events):
		self.debug("handle_events")
		for e in events:
			event_type = self.get_type_of_event(e)
			value = self.get_value_from_event(e, event_type)

			if value:
				try:
					data = self.controlls[str(value)]
				except:
					pass
				else:
					if "k_hold" in data["type"]:
						if event_type == "k_down":
							self.active_command(data["function"])
						else:
							if event_type == "k_up":
								self.inactive_command(data["function"])
					else:
						if "click" in data["type"]:
							x, y = self.visuals.get_mouse_pos()
							data["function"](x, y)
						else:
							if event_type in data["type"]:
								data["function"]()


		for c in self.active_commands:
			c()



	def __init__(self, keys_map, pygame, debug, main):
		self.debug = debug.get_debug("CONTROLLS")
		self.debug("__init__")

		self.pygame = pygame

		self.main = main

		self.phisics = self.main.phisics

		self.visuals = self.main.visuals

		self.keys_map = keys_map
		
		self.types = {"scroll":[pygame.MOUSEBUTTONDOWN], "k_down":[pygame.KEYDOWN], "k_up":[pygame.KEYUP], "k_hold":[pygame.KEYDOWN, pygame.KEYUP, "k_hold"], "click":[pygame.MOUSEBUTTONDOWN, "click"]}

		self.keys = {"k_f":pygame.K_f, "k_down":pygame.K_DOWN, "k_up":pygame.K_UP, "k_space":pygame.K_SPACE, "k_rshift":pygame.K_RSHIFT, "k_escape":pygame.K_ESCAPE, "k_a":pygame.K_a, "k_s":pygame.K_s, "k_d":pygame.K_d, "k_w":pygame.K_w, "k_r":pygame.K_r}

		self.commands = {"change_lvl":self.change_lvl, "spawn_new_rect":self.spawn_new_rect, "reload_lvl":self.reload_lvl, "object_move_forward":self.object_move_forward, "object_move_back":self.object_move_back, "object_move_left":self.object_move_left, "object_move_right":self.object_move_right, "switch_pause":self.switch_pause, "zoom_in":self.debug_zoom_in, "zoom_out":self.debug_zoom_out, "debug_down":self.debug_down, "debug_up":self.debug_up, "switch_debug":self.switch_debug}
		
		self.active_commands = [] 

		self.controlls = {}

		self.actions = []

		self.pause = False