from main.phisics import *
from main.visuals import *
from main.debug import *
from main.controlls import *
import time
import copy
from json import loads

class Simulation:
	def main(self):
		for i in range(10000):
			self.reload()
			self.debug("main", sep="Reload")

	def reload(self):
		self.debug("reload")
		self.controlls.handle_events(self.controlls.actions)
		self.controlls.actions = self.visuals.reload(self.phisics.objects)

	def setup(self):
		self.debug("setup")
		self.controlls.setup_controlls(self.controlls.keys_map)

	def load(self, lvl):
		self.debug("load", args=[lvl])
		data = loads(open("data/{}.json".format(lvl), "r").read())
		try:
			self.phisics.add_objects(data["objects"])
		except Exception as p:
			self.debug("load", error=p)

	def start(self):
		self.debug("start")
		self.main()


	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", debug_interval_time=5, fps=60, keys_map=False, output_console=True):

		self.Debug = Debug(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, interval_time=debug_interval_time, output_console=output_console)

		self.debug = self.Debug.get_debug("Simulation", debug_mode)

		self.debug("__init__", sep="Start")

		self.phisics = PHISICS(debug=self.Debug, debug_mode=debug_mode)
		self.visuals = VISUALS(debug=self.Debug, debug_mode=debug_mode, fps=fps)

		self.controlls = CONTROLLS(keys_map, pygame, self.Debug, debug_mode, self)

		self.debug_mode = debug_mode












