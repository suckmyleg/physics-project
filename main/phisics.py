
class PHISICS:
	def debug(self, function_name, args=False):
		if self.debug_function:
			self.debug_function("PHISICS", function_name, args=False)

	def main(self):
		self.debug("main")

	def __init__(self, debug=False):
		self.debug_function = debug
		self.debug("__init__")
