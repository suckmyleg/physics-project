from threading import Thread
from time import sleep, time
from main.phisics import Object
import json

def object_copy(instance, init_args=None):
    if init_args:
        new_obj = instance.__class__(**init_args)
    else:
        new_obj = instance.__class__()
    if hasattr(instance, '__dict__'):
        for k in instance.__dict__ :
            try:
                attr_copy = copy.deepcopy(getattr(instance, k))
            except Exception as e:
                attr_copy = object_copy(getattr(instance, k))
            setattr(new_obj, k, attr_copy)

        new_attrs = list(new_obj.__dict__.keys())
        for k in new_attrs:
            if not hasattr(instance, k):
                delattr(new_obj, k)
        return new_obj
    else:
        return instance

class Loading_screen:
	def __init__(self, debug, visuals, phisics, main):
		self.debug = debug.get_debug("LOADING_SCREEN")
		self.debug("__init__")

		self.main = main
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
		if not self.loading:
			self.loading = True
			self.phisics.pause = True
			t = Thread(target=self.start, args=(len(objects), title))
			t.start()

			try:

				fun(objects, fun=self.add_loaded, fun_info=self.change_loading_message)

			except Exception as e:
				self.change_loading_message("Error loading\n{}".format(e))
				self.debug("load", error=e)

			self.loading = False

	def start(self, to_load, title):
		self.debug("start")
		self.loading = True
		self.total = to_load
		self.current = 0
		self.progress = 0
		self.loading_message = "Loading"
		self.loading_screen_title = title

		self.loading_screen()

		self.phisics.pause = False

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
	def __init__(self, debug, visuals, phisics, main):
		self.debug = debug.get_debug("ERROR_INFO")
		self.debug("__init__")

		self.main = main
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
		self.status = True
		self.phisics.pause = True
		while self.status:
			actions = self.reload_loading_screen()
		self.phisics.pause = False



	def start(self):
		self.debug("start")
		t = Thread(target=self.error).start()

class RECORDING:
	def __init__(self, debug, visuals, phisics, main):
		self.debug = debug.get_debug("RECORDING")
		self.debug("__init__")
		self.main = main
		self.visuals = visuals
		self.phisics = phisics
		self.recording = False
		self.recording_file = False
		self.objects_backup = [] 
		self.record_data = []
		self.status = False
		self.recording_fps = 90
		self.delay = 1 / self.recording_fps
		self.mode = 2
		self.save = False
		self.last_recording_file = False

	def save_recording_file(self, data=False):
		if not data:
			data = self.record_data
		print(json.dumps(data), file = self.recording_file)

	def grab_frames(self):
		self.debug("grab_frames")
		self.recording_name = "recordings/recording_{}.json".format(time())
		self.recording_file = open(self.recording_name, "w")
		while self.status:
			data = [o.toList() for o in self.phisics.objects]
			if self.mode == 2:
				self.save_recording_file(data)
			else:
				self.record_data.append(data)
			sleep(self.delay)
		if self.mode == 2:
			data_str = open(self.recording_name, "r").read()
			data_str.split("\n")
			self.recording_file.write(json.dumps(data_str))
		else:
			if self.save:
				self.save_recording_file()
		self.recording_file.close()

	def record(self):
		self.debug("record")
		print("Recording")
		self.recording = True
		self.record_data = []
		self.status = True
		Thread(target=self.grab_frames).start()

	def stop(self):
		self.debug("stop")
		print("Stopped recording")
		self.status = False

	def play(self):
		self.debug("play")
		self.phisics.pause = True
		self.objects_backup = self.phisics.objects
		self.phisics.objects = []
		self.main.main_status = False
		print("Playing...")
		if self.mode == 2:
			data = json.loads(open(self.recording_name, "r").read())
		else:
			data = self.record_data
			
		for objects in data:
			controlls_actions = self.visuals.reload([Object(self.phisics, *o) for o in objects], self.recording_fps)
		print("Finished playing")
		self.phisics.pause = False
		self.phisics.objects = self.objects_backup
		self.main.main_status = True

class MENUS:
	def setup_menus(self):
		self.debug("setup_menus")
		for m in self.menus:
			self.add_menu(m[1], m[0])
			self.start_menu(m[1])

	def start_menu(self, name):
		self.debug("start_menu")
		return setattr(self, name, self.get_menu_function(name)(self.Debug, self.visuals, self.phisics, self.main))

	def get_menu_function(self, name):
		self.debug("get_menu_function")
		return getattr(self, name+"_function")

	def get_menu(self, name):
		self.debug("get_menu")
		return getattr(self, name)

	def add_menu(self, name, menu):
		self.debug("add_menu")
		setattr(self, name+"_function", menu)
		self.n_menus += 1

	def __init__(self, debug, visuals, phisics, main):
		self.Debug = debug

		self.debug = self.Debug.get_debug("MENUS")
		self.debug("__init__")

		self.visuals = visuals

		self.phisics = phisics

		self.main = main

		self.menus = [[Loading_screen, "loading_screen"], [Error_info , "getting_error_info"], [RECORDING, "recording"]]

		self.n_menus = 0

		self.setup_menus()
