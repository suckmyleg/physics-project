from main.phisics import *
from main.visuals import *
from time import time, sleep

class Debug:
	def time_passed(self):
		return int(time() - self.start_time)

	def space(self):
		pass

	def clean_args(self, args, s="(", e=")"):
		if args:
			args = "{}{}{}".format(s, args, e)
		else:
			args = "{}{}".format(s, e)
		return args

	def deb_2(self, main, function_name, args):

		datas = [
		["%M", main],
		["%F", function_name],
		["%A", args],
		["%T", self.time_passed()],
		["%I", self.debug_n]
		]

		t = self.reactive_deb

		for d in datas:

			t = t.replace(d[0], str(d[1]))

		print(t)

	def deb_1(self, main, function_name, args):
		args = self.clean_args(args)

		print("")

	def deb_0(self, main, function_name, args):
		args = self.clean_args(args)

		print("[{}] {} {}.{}{}".format(self.debug_n, self.time_passed(), main, function_name, args))

	def debug(self, main, function_name, args=False):
		if self.display_log:

			self.debug_n += 1
				
			self.modes[self.debug_mode](main, function_name, args)

	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I"):
		self.display_log = log
		self.start_time = time()
		self.debug_n = 0
		self.debug_mode = debug_mode
		self.modes = [self.deb_0, self.deb_1, self.deb_2]
		self.reactive_deb = debug_reactive




class Simulation:
	def debug(self, function_name, args=False):
		self.Debug.debug("Simulation", function_name, args)


	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I"):
		self.Debug = Debug(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive)
		self.debug("__init__")


		self.phisics = PHISICS(debug=self.Debug.debug)
		self.visuals = VISUALS(debug=self.Debug.debug)


	def setup(self):
		self.debug("setup")

	def load(self, lvl):
		self.debug("load", args=[lvl])

		

	def start(self):
		self.debug("start")