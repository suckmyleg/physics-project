import numpy as np
import math
import copy

class PHISICS:
	def main(self):
		self.debug("main")

	def reload(self):
		self.debug("reload")
		for o in self.objects:
			self.act_react(o)

	def act_react(self, o):
		self.debug("act_react")
		self.act_to_object(o)
		self.react_to_movement(o)

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

	def real_speed(self, speed):
		return speed/self.get_fps()

	def act_to_object(self, o):
		self.debug("act_to_object")
		if not o["collider"]["static"]:
			self.react(o)


	def react_to_movement(self, o):
		self.debug("react_to_movement")
		if not o["collider"]["movement"]["x"] == 0 or not o["collider"]["movement"]["y"] == 0:
			self.move_rect(o, o["collider"]["movement"]["x"], o["collider"]["movement"]["y"])


	def move_line(self, o, x, y):
		self.debug("move_line")
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
		if self.collider_phisics:
			n = self.get_nearest_distance(rect)
			if n < x:
				x = n

		rect["collider"]["body"]["x"] += x
		rect["collider"]["body"]["y"] += y

		for v in rect["collider"]["body"]["vectors"]:
			v[0] += x
			v[1] += y

		return x, y


	def push_rect(self, rect, x, y):
		self.debug("push_rect")
		rect["collider"]["movement"]["x"] += self.real_speed(x)
		rect["collider"]["movement"]["y"] += self.real_speed(y)

	def move_rect(self, rect, x, y):
		self.debug("move_rect")
		x, y = self.move_collider_rect(rect, x, y)
		self.move_visual_rect(rect, x, y)

	def fx_fy(self, i, angle):
		self.debug("fx_fy")
		return math.sin(angle)*i, math.cos(angle)*i

	def get_angle_from_x_y(self, x, y):
		self.debug("get_angle_from_x_y")

		if x == 0:
			return 0

		angle = 0

		if x < 0 or y < 0:
			angle += 0

		angle += math.atan(y/x)

		print(angle, y, x)
		return angle


	def react(self, objectt):
		self.debug("react")
		for o in self.objects:
			if not objectt == o:
				fx, fy = self.get_act_x_y(objectt, o)
				self.push_rect(o, fx, fy)

	def get_gravity_intensity(self, r, m):
		self.debug("get_gravity_intensity")
		return (-self.constants["G"]*(m/(r**2)))

	def get_act_x_y(self, obj1, obj2):
		self.debug("act_to_objects")
		x, y, h = self.distance_beetween_rects_centers(obj1, obj2)

		i = self.get_gravity_intensity(h, obj1["collider"]["mass"])


		if not x == 0 and not y == 0:

			angle = self.get_angle_from_x_y(x, y)
			
			fx, fy = self.fx_fy(i, angle)
			
			#print(x, y, h, i, angle, fx, fy)
		else:
			if x == 0:
				fx = 0
				fy = i
			else:
				if y == 0:
					fx = i
					fy = 0

		return fx, fy



	def get_nearest_distance(self, rect):
		near = False
		for o in self.objects:
			n = self.distance_beetween_rects(rect, o)
			if not near:
				near = n
			else:
				if near > n:
					near = n
		self.debug("get_nearest_distance", args=[near])
		return abs(near)

	def distance_beetween_rects(self, obj1, obj2):
		self.debug("distance_beetween_rects")
		return self.distance_beetween_rects(obj1["collider"]["body"], obj2["collider"]["body"])

	def distance_beetween_rects_centers(self, obj1, obj2):
		self.debug("distance_beetween_rects_centers")
		x = obj1["collider"]["body"]["vectors"][4][0] - obj2["collider"]["body"]["vectors"][4][0]
		y = obj1["collider"]["body"]["vectors"][4][1] - obj2["collider"]["body"]["vectors"][4][1]

		if y == 0:
			return x, y, x
		else:
			if x == 0:
				return x, y, y

		return x, y, math.sqrt(((x)**2)+ ((y)**2))


	def distance_beetween_rects(self, rect1, rect2):
		self.debug("distance_beetween_rects")
		return min(rect1["collider"]["body"]['x']+rect1["collider"]["body"]['w']-rect2["collider"]["body"]['x'], rect2["collider"]["body"]['x']+rect2["collider"]["body"]['w']-rect1["collider"]["body"]['x'])


	def find_point_in_area(self, x1, y1, x2, y2, x, y):
		self.debug("find_point_in_area")
		if (x > x1 and x < x2 and y > y1 and y < y2):
			return True
		else:
			return False

	def point_in_area(self, area, x, y):
		self.debug("point_in_area")
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
			[body["x"] + body["w"], body["y"] + body["h"]],
			[body["x"] + (body["w"]/2), body["y"] + (body["h"]/2)]
		]
		return body

	def setup_collider(self, collider):
		self.debug("setup_collider")
		collider["body"] = self.setup_rect_body(collider["body"])
		collider["mass"] = 10000000000000000
		collider["movement"] = {"x":0, "y":0}
		return collider
 
	def create_object(self, json_object):
		self.debug("create_object", args=[json_object])

		json_object["label"] = "Test"

		json_object["collider"] = self.setup_collider(json_object["collider"])

		return json_object

	def setup_objects(self, objectss):
		self.debug("setup_objects", args=[objectss])
		objects = copy.deepcopy(objectss)
		for o in objects:
			self.add_object(self.create_object(o))

	def __init__(self, debug, debug_mode, get_fps):
		self.debug = debug.get_debug("PHISICS", debug_mode)
		self.debug("__init__")

		self.get_fps = get_fps

		self.constants = {"G":6.67*10**(-11)}

		self.collider_phisics = False

		self.objects = []
