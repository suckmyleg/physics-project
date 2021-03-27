from main.phisics import *
from main.visuals import *
from main.debug import *

class Simulation:
	def debug(self, function_name, args=False):
		self.Debug.debug("Simulation", function_name, args)


	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", debug_interval_time=5):
		self.Debug = Debug(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, interval_time=debug_interval_time)
		self.debug("__init__")

		self.phisics = PHISICS(debug=self.Debug.debug)
		self.visuals = VISUALS(debug=self.Debug.debug)


	def setup(self):
		self.debug("setup")

	def load(self, lvl):
		self.debug("load", args=[lvl])

		
	def start(self):
		self.debug("start")