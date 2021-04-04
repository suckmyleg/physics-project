import numpy as np
import copy

class PHISICS:
	def main(self):
		self.debug("main")

	def load_objects(self, objects):
		self.debug("load_objects")
		self.objects = []
		self.setup_objects(objects)

	def add_objects(self, objects):
		self.debug("add_objects")
		self.setup_objects(objects)

	def add_object(self, o):
		self.debug("add_object", args=[o])
		self.objects.append(o)

	def create_point(self, P):
		self.debug("create_point")
		return np.array([P[0], P[1]])

	def AB(self, A, B):
		self.debug("AB")
		return [A, B, B-A]








	def move_line(self, o, x, y):
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


	def move_visual_rect(self, rect, x, y):
		self.debug("move_visual_rect")
		rect["visual"]["body"]["x"] += x
		rect["visual"]["body"]["y"] += y


	def move_collider_rect(self, rect, x, y):
		self.debug("move_collider_rect")
		n = self.get_nearest_distance(rect)
		if n < x:
			x = n

		rect["collider"]["body"]["x"] += x
		rect["collider"]["body"]["y"] += y

		return x, y


	def move_rect(self, rect, x, y):
		self.debug("move_rect")
		x, y = self.move_collider_rect(rect, x, y)
		self.move_visual_rect(rect, x, y)










	def get_nearest_distance(self, rect):
		near = False
		for o in self.objects:
			n = self.distance_beetween_objects_rects(rect, o)
			if not near:
				near = n
			else:
				if near > n:
					near = n
		self.debug("get_nearest_distance", args=[near])
		return abs(near)

	def distance_beetween_objects_rects(self, obj1, obj2):
		self.debug("distance_beetween_objects_rects")
		return self.distance_beetween_rects(obj1["collider"]["body"], obj2["collider"]["body"])

	def distance_beetween_rects(self, rect1, rect2):
		self.debug("distance_beetween_rects")
		return min(rect1['x']+rect1['w']-rect2['x'], rect2['x']+rect2['w']-rect1['x'])


	def find_point_in_area(self, x1, y1, x2, y2, x, y):
		if (x > x1 and x < x2 and y > y1 and y < y2):
			return True
		else:
			return False

	def point_in_area(self, area, x, y):
		x1 = area["x"]
		y1 = area["y"] + area["h"]

		x2 = area["x"] + area["w"]
		y2 = area["y"]

		return self.find_point_in_area(x1, y1, x2, y2, x, y)






	def get_rect_ect_from_2_points(self, A, B):
		self.debug("get_rect_ect_from_2_points")
		x = B[0] - A[0]
		y = B[1] - A[1]

		return [y, -x, -(A[0]*(y) - A[1]*(x))]




	def setup_line_body(self, body):
		self.debug("setup_line_body")
		try:
			body["A"] = self.create_point(body["A"])
			body["B"] =	self.create_point(body["B"])
			body["AB"] = self.AB(body["A"], body["B"])
			body["EC"] = self.get_rect_ect_from_2_points(body["A"], body["B"])
			return body
		except Exception as e:
			self.debug("setup_body", error=e)

	def setup_rect_body(self, body):
		self.debug("setup_rect_body")
		body["vectors"] = [
			[body["x"], body["y"]],
			[body["x"] + body["w"], body["y"]],
			[body["x"], body["y"] + body["h"]],
			[body["x"] + body["w"], body["y"] + body["h"]]
		]
		return body

	def setup_collider(self, collider):
		self.debug("setup_collider")
		collider["body"] = self.setup_rect_body(collider["body"])
		return collider
 
	def create_object(self, json_object):
		self.debug("create_object", args=[json_object])

		json_object["collider"] = self.setup_collider(json_object["collider"])

		return json_object

	def setup_objects(self, objectss):
		self.debug("setup_objects", args=[objectss])
		objects = copy.deepcopy(objectss)
		for o in objects:
			self.add_object(self.create_object(o))

	def __init__(self, debug, debug_mode):
		self.debug = debug.get_debug("PHISICS", debug_mode)
		self.debug("__init__")

		self.objects = []
