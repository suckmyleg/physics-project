import numpy as np
import math
import copy
from time import sleep

class PHISICS:
	def main(self):
		self.debug("main")

	def reload(self):
		self.debug("reload")
		if not self.pause:
			for o in self.objects:
				self.act_react(o)

	def act_react(self, o):
		self.debug("act_react")
		self.act_to_object(o)
		self.react_to_movement(o)

	def load_objects(self, objects, fun=False, fun_info=False):
		self.debug("load_objects")
		self.objects = []
		self.setup_objects(objects, fun=fun, fun_info=fun_info)

	def add_objects(self, objects, fun=False, fun_info=False):
		self.debug("add_objects")
		self.setup_objects(objects, fun=fun, fun_info=fun_info)

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
			n, nearest_object, angle = self.get_nearest_distance(rect)
			rect["collider"]["object_nearest"] = n

			xx, yy = self.fx_fy(n, angle)

			if x > 0:
				if n < x:
					x = n

			if y > 0:
				if n < y:
					y = n
			if n < x or n < y:
				xm = (rect["collider"]["movement"]["x"] + nearest_object["collider"]["movement"]["x"])/2
				ym = (rect["collider"]["movement"]["y"] + nearest_object["collider"]["movement"]["y"])/2

				rect["collider"]["movement"]["x"] = xm
				rect["collider"]["movement"]["y"] = ym
				nearest_object["collider"]["movement"]["x"] = xm
				nearest_object["collider"]["movement"]["y"] = ym

				self.move_collider_rect_without_passion(nearest_object, xm, ym)

			return self.move_collider_rect_without_passion(rect, x, y)

	def move_collider_rect_without_passion(self, rect, x, y):
		self.debug("move_collider_rect")

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
			if y >= 0:
				return 180
			else:
				return 0

		if x < 0:
			if y > 0:
				angle = 90
			else:
				angle = 0

		else:
			if y > 0:
				angle = 90
			else:
				angle = 180

		angle += abs(math.atan(y/x))

		#print("x:{} y:{} angle:{}".format(x, y, angle))

		return angle


	def react(self, objectt):
		self.debug("react")
		for o in self.objects:
			if not objectt == o:
				fx, fy = self.get_act_x_y(objectt, o)
				self.push_rect(o, fx, fy)

	def get_gravity_intensity(self, r, m, M):
		self.debug("get_gravity_intensity")
		if r > 0:
			return (-self.constants["G"]*(m/((r*self.distance_scale)**2))*M)
		else:
			return 0

	def get_act_x_y(self, obj1, obj2):
		self.debug("act_to_objects")
		x, y, h = self.distance_beetween_rects_centers(obj1, obj2)

		i = self.get_gravity_intensity(h, obj1["collider"]["mass"], obj2["collider"]["mass"])

		if not x == 0 and not y == 0:

			angle = self.get_angle_from_x_y(x, y)


			fx, fy = self.fx_fy(i, angle)
			
		else:
			if x == 0:
				fx = 0
				fy = -i
			else:
				if y == 0:
					fx = -i
					fy = 0

		#print(fx, fy)

		return -fx, -fy



	def get_nearest_distance(self, rect):
		near = False
		n_o = False
		angle = False
		for o in self.objects:
			if not rect == o:
				n, ang = self.distance_beetween_rects(rect, o)
				if not near:
					near = n
					n_o = o
					angle = ang
				else:
					if near > n:
						near = n
						n_o = o
						angle = ang
		self.debug("get_nearest_distance", args=[near])
		return abs(near), n_o, angle

	def distance_beetween_rects_centers(self, obj1, obj2):
		self.debug("distance_beetween_rects_centers")
		x = obj2["collider"]["body"]["vectors"][4][0] - obj1["collider"]["body"]["vectors"][4][0]
		y = obj2["collider"]["body"]["vectors"][4][1] - obj1["collider"]["body"]["vectors"][4][1]

		if y == 0:
			return x, y, x
		else:
			if x == 0:
				return x, y, y

		return x, y, self.get_hipo(x, y)

	def get_hipo(self, x, y):
		self.debug("get_hipo")
		return math.sqrt(((x)**2)+ ((y)**2))

	def beetween(self, n1, n2, v):
		self.debug("move_collider_rect")
		if n1 < v < n2:
			return True
		else:
			return False

	def get_hipo_inside_rect(self, rect1, rect2, x, y):

		self.debug("move_collider_rect")
		if x == 0:
			return y - (rect1["collider"]["body"]["h"]/2) - (rect2["collider"]["body"]["h"]/2)
		else:
			if y == 0:
				return x - (rect1["collider"]["body"]["w"]/2) - (rect2["collider"]["body"]["w"]/2)  
 	
		angle = self.get_angle_from_x_y(x, y)

		if self.beetween(360-rect1["collider"]["body"]["vectors_angles"][2], 360, angle) or self.beetween(0, rect1["collider"]["body"]["vectors_angles"][3], angle) or self.beetween(rect1["collider"]["body"]["vectors_angles"][1], rect1["collider"]["body"]["vectors_angles"][0], angle):
			c = rect1["collider"]["body"]["h"]
		else:
			c = rect1["collider"]["body"]["w"]

		angle = angle%90

		if angle == 0:
			return 0

		return c/(math.sin(angle))

	def distance_beetween_rects(self, rect1, rect2):
		self.debug("distance_beetween_rects")
		x = rect2["collider"]["body"]["vectors"][4][0] - rect1["collider"]["body"]["vectors"][4][0]
		y = rect2["collider"]["body"]["vectors"][4][1] - rect1["collider"]["body"]["vectors"][4][1]
		total = self.get_hipo(x, y)

		#l1 = self.get_hipo_inside_rect(rect1, rect2, x, y)
		#l2 = self.get_hipo_inside_rect(rect2, rect1, x, y)

		h = total

		return abs(h - rect1["collider"]["body"]["w"]), self.get_angle_from_x_y(x, y)


		


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
			[body["x"] + body["w"], body["y"] + body["h"]]
		]
		center = [body["x"] + (body["w"]/2), body["y"] + (body["h"]/2)]

		body["vectors_angles"] = []

		for v in body["vectors"]:
			body["vectors_angles"].append(self.get_angle_from_x_y(v[0]-center[0], v[1]-center[1]))

		body["vectors"].append(center)

		return body

	def setup_collider(self, collider):
		self.debug("setup_collider")
		collider["body"] = self.setup_rect_body(collider["body"])
		try:
			mov = collider["movement"]
		except:
			collider["movement"] = {"x":0, "y":0}
		else:
			if not mov:
				collider["movement"] = {"x":0, "y":0}
		return collider
 
	def create_object(self, json_object):
		self.debug("create_object", args=[json_object])

		json_object["label"] = "Test"

		json_object["collider"] = self.setup_collider(json_object["collider"])

		return json_object

	def setup_objects(self, objectss, fun=False, fun_info=False):
		self.debug("setup_objects", args=[objectss])
		objects = copy.deepcopy(objectss)
		i = 0
		for o in objects:
			i += 1
			if fun_info:
				fun_info("Adding object n: {}/{}".format(i, len(objects)))
			self.add_object(self.create_object(o))
			if fun:
				fun()

	def __init__(self, debug, debug_mode, get_fps):
		self.debug = debug.get_debug("PHISICS", debug_mode)
		self.debug("__init__")

		self.get_fps = get_fps

		self.distance_scale = 1/1000

		self.pause = False

		self.constants = {"G":6.67*10**(-11)}

		self.collider_phisics = True

		self.objects = []
