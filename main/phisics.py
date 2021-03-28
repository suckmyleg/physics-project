import numpy as np
import copy

class PHISICS:
	def debug(self, function_name, args=False, sep=False):
		if self.debug_function:
			self.debug_function("PHISICS", function_name, args=False, sep=sep)

	def main(self):
		self.debug("main")

	def load_objects(self, objects):
		self.debug("load_objects")
		self.objects = []
		self.setup_objects(objects)

	def add_objects(self, objects):
		self.debug("add_objects")
		self.setup_objects(objects)

	def create_point(self, P):
		self.debug("create_point")
		return np.array([P[0], P[1]])

	def AB(self, A, B):
		self.debug("AB")
		return [A, B, B-A]

	def move_object(self, o, x, y):
		self.debug("move_object")
		for b in o["collider"]["body"]:
			b["A"][0] = b["A"][0] + x
			b["A"][1] = b["A"][1] + y

			b["B"][0] = b["B"][0] + x
			b["B"][1] = b["B"][1] + y

			b["AB"] = self.AB(b["A"], b["B"])
			b["EC"] = self.get_rect_ect_from_2_points(b["A"], b["B"])

		for b in o["visual"]["body"]:
			b["A"][0] = b["A"][0] + x
			b["A"][1] = b["A"][1] + y

			b["B"][0] = b["B"][0] + x
			b["B"][1] = b["B"][1] + y


	def get_rect_ect_from_2_points(self, A, B):
		self.debug("get_rect_ect_from_2_points")
		x = B[0] - A[0]
		y = B[1] - A[1]

		return [y, -x, -(A[0]*(y) - A[1]*(x))]

	def setup_body(self, body):
		self.debug("setup_body")
		body["A"] = self.create_point(body["A"])
		body["B"] =	self.create_point(body["B"])
		body["AB"] = self.AB(body["A"], body["B"])
		body["EC"] = self.get_rect_ect_from_2_points(body["A"], body["B"])
		return body

	def setup_collider(self, collider):
		self.debug("setup_collider")
		for b in collider["body"]:
			b = self.setup_body(b)
		return collider
 
	def create_object(self, json_object):
		self.debug("create_object")

		json_object["collider"] = self.setup_collider(json_object["collider"])

		return json_object

	def setup_objects(self, objectss):
		self.debug("setup_objects")
		objects = copy.deepcopy(objectss)
		for o in objects:
			self.objects.append(self.create_object(o))
		return objects

	def __init__(self, debug=False):
		self.debug_function = debug
		self.debug("__init__")

		self.objects = []
