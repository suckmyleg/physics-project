from main.phisics import *
from main.visuals import *
from main.debug import *
from main.controlls import *
from main.menus import *
import time
import copy
from json import loads
from time import sleep


class Simulation:
	def main(self):
		for i in range(100000000):
			self.reload()
			self.debug("main", sep="Reload")

	def reload(self):
		self.debug("reload")
		if self.main_status:
			try:
				self.controlls.handle_events(self.controlls.actions)
				self.phisics.reload()
				self.controlls.actions = self.visuals.reload(self.phisics.objects)
			except Exception as e:
				self.debug("reload", error=e)
		else:
			sleep(0.5)


	def setup(self):
		self.debug("setup")
		self.controlls.setup_controlls(self.controlls.keys_map)

	def reload_lvl(self):
		self.debug("reload_lvl")
		self.load_lvl(self.actual_lvl)

	def load_lvl(self, lvl):
		self.debug("load_lvl", args=[lvl])
		self.phisics.objects = []
		self.actual_lvl = lvl
		data = loads(open("data/{}.json".format(lvl), "r").read())

		self.phisics.distance_scale = data["settings"]["scale"]

		self.menus.loading_screen.load(self.phisics.add_objects, data["objects"])

	def start(self):
		self.debug("start")
		self.main()


	def get_fps(self):
		self.debug("get_fps")
		return self.visuals.current_fps

	def __init__(self, log_active=False, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", debug_interval_time=5, fps=60, keys_map=False, output_console=True, output_file=False):

		self.Debug = Debug(self, log_active, log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, interval_time=debug_interval_time, output_console=output_console, output_file=output_file)

		self.debug = self.Debug.get_debug("Simulation", debug_mode)

		self.debug("__init__", sep="Start")

		self.actual_lvl = False

		self.phisics = PHISICS(self.Debug, self.get_fps)
		self.visuals = VISUALS(self.phisics, debug=self.Debug, fps=fps, main=self)

		self.controlls = CONTROLLS(keys_map, pygame, self.Debug, self)

		self.menus = MENUS(self.Debug, self.visuals, self.phisics, self)

		self.to_load = 0

		self.loaded = 0

		self.loading = False

		self.main_status = True

		self.debug_mode = debug_mode












