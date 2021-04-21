from threading import Thread

class Loading_screen:
	def __init__(self, debug, visuals, phisics):
		self.debug = debug.get_debug("LOADING_SCREEN")
		self.debug("__init__")

		self.visuals = visuals
		self.phisics = phisics
		self.loading = False

		self.loading_message = "Loading"
		self.loading_screen_title = "Loading"
		self.total = 0
		self.current = 0
		self.progress = 0

		self.progress_border_size = 5
		self.height_bar = 40


	def load(self, fun, objects, title="Loading"):
		self.phisics.pause = True
		t = Thread(target=self.start, args=(len(objects), title))
		t.start()

		try:

			fun(objects, fun=self.add_loaded, fun_info=self.change_loading_message)

		except Exception as e:
			self.change_loading_message("Error loading\n{}".format(e))
			self.debug("load", error=e)

		self.loading = False

		self.phisics.pause = False

	def start(self, to_load, title):
		self.debug("start")
		self.loading = True
		self.total = to_load
		self.current = 0
		self.progress = 0
		self.loading_message = "Loading"
		self.loading_screen_title = title

		self.loading_screen()

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

		color_bar = (0, 255, int(160*(self.progress/100)))

		width = self.visuals.width - 40
		
		width_bar = width*(self.progress/100)

		x = xs + self.visuals.width - 20 - width
		y = ys + self.visuals.height - 10 - self.height_bar

		middle_bar_x = x+(width_bar/2)
		middle_bar_y = y+(self.height_bar/2)

		progress_message = str(int(self.progress))+"%"

		self.display_loading_bar_message(x+5, y)

		self.visuals.pygame.draw.rect(self.visuals.screen, (0,0,0), self.visuals.pygame.Rect(x, y, width, self.height_bar))

		self.visuals.pygame.draw.rect(self.visuals.screen, color_bar, self.visuals.pygame.Rect(x+self.progress_border_size ,y+self.progress_border_size, width_bar-self.progress_border_size, self.height_bar-self.progress_border_size*2))

		label_color = (abs(200-color_bar[0]),abs(255-color_bar[1]),abs(250-color_bar[2]))

		if len(progress_message)*12 < width_bar:

			porcentage_label = self.visuals.myFont.render(progress_message, True, label_color)

			self.visuals.screen.blit(porcentage_label, (middle_bar_x - len(progress_message), middle_bar_y-self.visuals.font_size/2))

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
		try:
			while self.loading:
				self.debug("loading_screen", sep="Loading {}".format(self.progress))

				self.reload_loading_screen()

			self.change_loading_message("Done!")

			self.reload_loading_screen()

		except Exception as e:
			self.debug("loading_screen", error=e)


		

class Error_info:
	def __init__(self, debug, visuals, phisics):
		self.debug = debug.get_debug("ERROR_INFO")
		self.debug("__init__")

		self.visuals = visuals
		self.phisics = phisics

	def display_message(self, color=(0,128,255)):
		self.debug("display_message")

		message = "An error ocurred. Wait until the data is compiled."

		label = self.visuals.myFont.render(str(message), True, color)
		self.visuals.screen.blit(label, ((self.visuals.width-len(message))/2, 200))

	def reload_loading_screen(self):
		self.debug("reload_loading_screen")
		actions = self.visuals.get_actions()
		self.visuals.clear_screen(color=(0, 0, 100))
		self.display_message()
		self.visuals.screen_info()
		self.visuals.update_screen()
		return actions

	def done(self):
		self.status = False

	def error(self):
		self.debug("error")
		while self.status:
			actions = self.reload_loading_screen()



	def start(self):
		self.debug("start")
		self.status = True
		t = Thread(target=self.error).start()


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

		self.menus = [[Loading_screen, "loading_screen"], [Error_info , "getting_error_info"]]

		self.n_menus = 0

		self.setup_menus()