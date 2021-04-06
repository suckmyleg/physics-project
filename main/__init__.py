from main.phisics import *
from main.visuals import *
from main.debug import *
from main.controlls import *
import time
import copy
from json import loads

class Simulation:
	def main(self):
		for i in range(100000000):
			self.reload()
			self.debug("main", sep="Reload")

	def reload(self):
		self.debug("reload")
		self.controlls.handle_events(self.controlls.actions)
		self.phisics.reload()
		self.controlls.actions = self.visuals.reload(self.phisics.objects)

	def setup(self):
		self.debug("setup")
		self.controlls.setup_controlls(self.controlls.keys_map)

	def reload_lvl(self):
		self.debug("reload_lvl")
		self.load_lvl(self.actual_lvl)

	def get_progress(self):
		self.debug("get_progress")
		if self.loaded == 0:
			return 0
		return (self.loaded * 100)/self.to_load

	def check_loading(self):
		self.debug("check_loading")
		return self.loading

	def add_loaded(self):
		self.debug("add_loaded")
		self.loaded += 1

	def load_lvl(self, lvl):
		self.debug("load_lvl", args=[lvl])
		self.phisics.objects = []
		self.actual_lvl = lvl
		data = loads(open("data/{}.json".format(lvl), "r").read())
		self.to_load = len(data["objects"])
		self.loaded = 0
		self.loading = True
		change_message = self.visuals.start_loading_screen(self.check_loading, self.get_progress)
		try:
			self.phisics.add_objects(data["objects"], fun=self.add_loaded, fun_info=change_message)
		except Exception as p:
			self.debug("load_lvl", error=p)

		self.loading = False

	def start(self):
		self.debug("start")
		self.main()


	def get_fps(self):
		self.debug("get_fps")
		return self.visuals.fps

	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", debug_interval_time=5, fps=60, keys_map=False, output_console=True, output_file=False):

		self.Debug = Debug(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, interval_time=debug_interval_time, output_console=output_console, output_file=output_file)

		self.debug = self.Debug.get_debug("Simulation", debug_mode)

		self.debug("__init__", sep="Start")

		self.actual_lvl = False

		self.phisics = PHISICS(self.Debug, debug_mode, self.get_fps)
		self.visuals = VISUALS(debug=self.Debug, debug_mode=debug_mode, fps=fps)

		self.controlls = CONTROLLS(keys_map, pygame, self.Debug, debug_mode, self)

		self.to_load = 0

		self.loaded = 0

		self.loading = False

		self.debug_mode = debug_mode












