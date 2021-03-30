from time import time, sleep

class Minidebug:
	def __init__(self, main, mode, debug_reactive, fun):
		self.main = main
		self.mode = mode
		self.debug_reactive = debug_reactive
		self.function = fun

	def debug(self, function_name, args=[], error=False, sep=False):
		self.function(self.main, function_name, args, error=error, debug_reactive=self.debug_reactive, mode=self.mode, sep=sep)

class Debug:
	def time_passed_float(self):
		return time() - self.start_time

	def time_passed(self):
		return int(self.time_passed_float()*100)/100

	def space(self, m1, m2, space_length=50, spacer=" "):
		t = ""
		length = space_length - len(m1)
		if length > 0:
			t = spacer*length
		return "{}{}{}".format(m1, t, m2)
			 

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
		return int(self.time_passed_float_interval()*100)/100

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

	def ceros(self, t):
		t = str(int(t*100))

		ll = len(t) - 2

		return t[:ll] + '.' + t[ll:]



	def pr(self, m, error=False):
		if error:
			m = m + " - ERROR: " + str(error)
		self.messages.append(m)
		if self.output_console:
			print(m)

	def deb_5(self, main, function_name, args, error=False, debug_reactive=""):
		args = self.clean_args(args)

		i1 = "{}.{}{} ".format(main, function_name, args)

		i2 = self.space(self.space(f"t:[{self.ceros(self.time_passed_float())}]", f"m:[{self.media()}/s]", space_length=12), f"mi:[{self.interval_media()}/s]", space_length=25)

		self.pr(self.space(i1, i2, space_length=45), error=error)

	def deb_4(self, main, function_name, args, error=False, debug_reactive=""):
		args = self.clean_args(args)

		self.pr("[{}] {}.{}{}".format(int(self.time_passed_float()), main, function_name, args), error=error)

	def deb_3(self, main, function_name, args, error=False, debug_reactive=""):
		args = self.clean_args(args)

		self.pr("[{}/s] [{}] [{}] {}.{}{}".format(self.interval_media(), self.debug_n, self.ceros(self.time_passed_float()), main, function_name, args), error=error)

	def deb_2(self, main, function_name, args, debug_reactive=False, error=False):

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

		if not debug_reactive:
			debug_reactive = self.debug_reactive
		t = debug_reactive

		for d in datas:
			r = d[1]
			if d[2]:
				r = r()
			t = t.replace(d[0], str(r))

		self.pr(t, error=error)

	def deb_1(self, main, function_name, args, error=False, debug_reactive=""):
		args = self.clean_args(args)

		self.pr("[{}/s] [{}] [{}] {}.{}{}".format(self.media(), self.debug_n, self.time_passed(), main, function_name, args), error=error)

	def deb_0(self, main, function_name, args, error=False, debug_reactive=""):
		args = self.clean_args(args)

		self.pr("[{}] {} {}.{}{}".format(self.debug_n, self.time_passed(), main, function_name, args), error=error)

	def debug(self, main, function_name, args=False, sep=False, error=False, mode=False, debug_reactive=""):
		if not mode:
			mode = self.debug_mode
		if self.display_log:

			self.debug_n += 1
			self.debug_n_interval += 1
				
			if sep:
				self.messages = []
				self.pr("\n-------{}".format(sep))

			self.modes[mode](main, function_name, args, error=error, debug_reactive=debug_reactive)

	def get_debug(self, main, mode, reactive=""):
		d = Minidebug(main, mode, reactive, self.debug)
		return d.debug

	def __init__(self, log=False, debug_mode=0, debug_reactive="%T -- %M.%F(%A) %I", interval_time=5, output_console=False):
		self.display_log = log
		if not self.display_log:
			output_console = False
		self.output_console = output_console
		self.start_time = time()
		self.start_time_interval = time()
		self.debug_n = 0
		self.debug_n_interval = 0
		self.interval_time = interval_time
		self.debug_mode = debug_mode
		self.modes = [self.deb_0, self.deb_1, self.deb_2, self.deb_3, self.deb_4, self.deb_5]
		self.debug_reactive = debug_reactive
		self.messages = []