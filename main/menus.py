from threading import Thread

class Loading_screen:
	def __init__(self, debug, visuals, p):
		self.debug = debug.get_debug("LOADING_SCREEN")
		self.debug("__init__")

		self.visuals = visuals
		self.loading = False

		self.loading_message = ""
		self.loading_screen_title = ""
		self.total = 0
		self.current = 0
		self.progress = 0

	def start(self, to_load, title):
		self.debug("start")
		self.loading = True
		self.total = to_load
		self.current = 0
		self.progress = 0
		self.loading_screen_title = title

		self.start_visual_menu()

	#LOGIC

	def reload_progress(self):
		self.debug("reload_progress")
		if self.current == 0:
			self.progress = 0
		self.progress = (self.current * 100)/self.total

		if self.progress == 100:
			self.loading = False

	def add_loaded(self):
		self.debug("add_loaded")
		self.current += 1
		self.reload_progress()

	#VISUAL

	def display_loading_bar_message(self, x, y):
		self.debug("display_loading_bar_message")

		title = self.visuals.myFont.render(str(self.loading_message), True, (255,0,0))
		self.visuals.screen.blit(title, (x, y-self.visuals.font_size*2))

	def display_progress(self, xs=0, ys=0):
		self.debug("display_progress")

		color_progress = (0, 255, int(160*(self.progress/100)))


		width = self.visuals.width - 40
		height = 20
		
		width_progress = width*(self.progress/100)

		x = xs + self.visuals.width - 20 - width
		y = ys + self.visuals.height - 10 - height

		middle_bar_x = x+(width_progress/2)
		middle_bar_y = y+(height/2)

		progress_message = str(int(self.progress))+"%"

		self.display_loading_bar_message(x+5, y)

		self.visuals.pygame.draw.rect(self.visuals.screen, (0,0,0), self.visuals.pygame.Rect(x, y, width, height))
		self.visuals.pygame.draw.rect(self.visuals.screen, color_progress, self.visuals.pygame.Rect(x ,y, width_progress, height))

		label_color = (abs(200-color_progress[0]),abs(255-color_progress[1]),abs(250-color_progress[2]))

		label = self.visuals.myFont.render(progress_message, True, label_color)
		self.visuals.screen.blit(label, (middle_bar_x - len(progress_message), middle_bar_y-self.visuals.font_size/2))

	def display_message(self, color=(0,128,255)):
		self.debug("display_message")

		label = self.visuals.myFont.render(str(self.loading_screen_title), True, color)
		self.visuals.screen.blit(label, ((self.visuals.width-len(self.loading_screen_title))/2, 200))


	def reload_loading_screen(self):
		self.debug("reload_loading_screen")
		actions = self.visuals.get_actions()
		self.visuals.clear_screen(color=(0, 0, 100))
		self.display_message()
		self.display_progress()
		self.visuals.screen_info()
		self.visuals.update_screen()
		return actions

	def change_loading_message(self, message):
		self.debug("change_loading_message")
		self.loading_message = str(message)

	def loading_screen(self):
		self.debug("loading_screen")
		print("Loading")
		while self.loading:

			self.reload_loading_screen()

		self.change_loading_message("Done!")

		self.reload_loading_screen()

	def start_visual_menu(self):
		self.debug("start_visual_menu")
		t = Thread(target=self.loading_screen)
		t.start()




class MENUS:
	def setup_menus(self):
		for m in self.menus:
			self.add_menu(m[1], m[0])
			self.start_menu(m[1])

	def start_menu(self, name):
		return setattr(self, name, self.get_menu_function(name)(self.Debug, self.visuals, self.phisics))

	def get_menu_function(self, name):
		return getattr(self, name+"_function")

	def get_menu(self, name):
		return getattr(self, name)

	def add_menu(self, name, menu):
		setattr(self, name+"_function", menu)
		self.n_menus += 1

	def __init__(self, debug, visuals, phisics):
		self.Debug = debug

		self.debug = self.Debug.get_debug("MENUS")
		self.debug("__init__")

		self.visuals = visuals

		self.phisics = phisics

		self.menus = [[Loading_screen, "loading_screen"]]

		self.n_menus = 0

		self.setup_menus()