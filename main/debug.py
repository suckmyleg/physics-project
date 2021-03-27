from time import time, sleep

class Debug:
	def time_passed_float(self):
		return time() - self.start_time

	def time_passed(self):
		return int(self.time_passed_float())

	def space(self):
		pass

	def clean_args(self, args, s="(", e=")"):
		if args:
			args = "{}{}{}".format(s, args, e)
		else:
			args = "{}{}".format(s, e)
		return args

	def media(self):
		t = self.time_passed_float()
		if t == 0:
			return self.debug_n
		return int(self.debug_n / t)

	def time_passed_float_interval(self):
		return time() - self.start_time_interval

	def time_passed_interval(self):
		return int(self.time_passed_float_interval())

	def interval_media(self):
		t = self.time_passed_float_interval()

		a = self.debug_n

		if not t == 0:
			a = int(self.debug_n_interval / t)
		
		#print(t, self.interval_time)

		if t >= self.interval_time:
			self.start_time_interval = time()
			self.debug_n_interval = 0

		return a

	def deb_2(self, main, function_name, args, reactive_deb=False):

		if not args:
			args = ""

		datas = [
		["%M", main, False],
		["%F", function_name, False],
		["%A", args, False],
		["%TI", self.time_passed_interval, True],
		["%SI", self.interval_media, True],
		["%T", self.time_passed, True],
		["%I", self.debug_n, False],
		["%S", self.media, True]
		]

		if not reactive_deb:
			reactive_deb = self.reactive_deb
		t = reactive_deb

		for d in datas:
			r = d[1]
			if d[2]:
				r = r()
			t = t.replace(d[0], str(r))

		print(t)

	def deb_1(self, main, function_name, args):
		args = self.clean_args(args)

		print("[{}/s] [{}] [{}] {}.{}({})".format(self.media(), self.debug_n, self.time_passed(), main, function_name, args))

	def deb_0(self, main, function_name, args):
		args = self.clean_args(args)

		print("[{}] {} {}.{}{}".format(self.debug_n, self.time_passed(), main, function_name, args))

	def debug(self, main, function_name, args=False):
		if self.display_log:

			self.debug_n += 1
			self.debug_n_interval += 1
				
			self.modes[self.debug_mode](main, function_name, args)

	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", interval_time=5):
		self.display_log = log
		self.start_time = time()
		self.start_time_interval = time()
		self.debug_n = 0
		self.debug_n_interval = 0
		self.interval_time = interval_time
		self.debug_mode = debug_mode
		self.modes = [self.deb_0, self.deb_1, self.deb_2]
		self.reactive_deb = debug_reactive