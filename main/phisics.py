import numpy as np
import math
import copy
from time import sleep

class Force:
	def __init__(self, conn, x=0, y=0, h=0, angle=0):
		self.conn = conn
		self.x = x
		self.y = y
		self.total_speed = x+y
		self.h = h
		self.angle = angle
		self.interactions = []

	def push_x_y(self, x, y):
		self.x += x
		self.y += y
		self.total_speed += x + y
		self.interactions.append([x, y])

	def stop(self):
		self.x = 0
		self.y = 0

	def reset(self):
		self.interactions = []

	def reload(self, fps=1):
		if not fps == 0:
			self.conn.x += self.x/fps
			self.conn.y += self.y/fps

class Object:
	def setup_vectors(self):
		self.center_vector = [self.x + self.width/2, self.y + self.height/2]

		self.vectors = [
			[self.x, self.y],
			[self.x+self.width, self.y],
			[self.x, self.y+self.height],
			[self.x+self.width, self.y+self.height]
		]


	def __init__(self, name="Object", x=0, y=0, speed=[0,0], width=5, height=5, static=False, mass=1, on_collission=False, color=[255, 0, 0]):
		self.name = name

		self.x = x
		self.y = y

		self.width = width
		self.height = height

		self.speed = Force(self, speed[0], speed[1])

		self.static = static

		self.layer = 1

		self.mass = mass

		self.color = color

		self.setup_vectors()

		self.on_collission = on_collission

	def stop(self):
		self.speed.stop()

	def move(self, speed):
		self.speed = speed

	def reload(self, fps=1):
		self.speed.reload(fps=fps)
		self.setup_vectors()

	def push(self, speed):
		self.speed.push_x_y(speed[0], speed[1])

class PHISICS:
	def main(self):
		self.debug("main")

	def reload(self):
		self.debug("reload")
		self.fps = self.get_fps()
		if not self.pause:
			for o in self.objects:
				o.speed.reset()
				self.act_react(o)

	def act_react(self, o):
		self.debug("act_react")
		self.react_to_objects(o)
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

	def real_speed(self, speed):
		return speed/self.get_fps()

	def react_to_objects(self, o):
		self.debug("react_to_objects")
		if not o.static:
			self.react(o)


	def react_to_movement(self, o):
		self.debug("react_to_movement")
		o.reload(fps=self.fps)


	def push_rect(self, rect, x, y):
		self.debug("push_rect")
		rect["collider"]["movement"]["x"] += self.real_speed(x)
		rect["collider"]["movement"]["y"] += self.real_speed(y)

	def fx_fy(self, i, angle):
		self.debug("fx_fy")
		return math.sin(math.radians(angle))*i*(-1), math.cos(math.radians(angle))*i*(-1)

	def get_angle_from_x_y(self, x, y):
		self.debug("get_angle_from_x_y")

		if x == 0:
			if y >= 0:
				return 0
			else:
				return 180

		if x < 0:
			if y > 0:
				angle = 270
			else:
				angle = 180

		else:
			if y > 0:
				angle = 0
			else:
				angle = 90

		a = math.degrees(abs(math.atan(y/x)))

		angle += a

		#print("x:{} y:{} a: {} angle:{}".format(x, y, a, angle))

		return angle


	def react(self, objectt):
		self.debug("react")
		for o in self.objects:
			if not objectt == o:
				self.push_from_gravity(objectt, o)

	def get_gravity_intensity(self, r, m, M):
		self.debug("get_gravity_intensity")
		r = abs(r)

		if r > 0:
			return (-self.constants["G"]*(M/((r*self.distance_scale)**2)))
		else:
			return 0

	def push_from_gravity(self, obj1, obj2):
		self.debug("push_from_gravity")

		x = (obj2.center_vector[0] - obj1.center_vector[0])*self.distance_scale
		y = ((obj2.center_vector[1] - obj1.center_vector[1])*self.distance_scale)

		if y == 0 or x == 0:
			h = x+y
		else:
			h = math.sqrt(((x)**2)+ ((y)**2))

		i = self.get_gravity_intensity(h, obj1.mass, obj2.mass)

		angle = self.get_angle_from_x_y(x, y)

		fx, fy = self.fx_fy(i, angle)

		obj1.push([fx, fy])


	def distance_beetween_rects_centers(self, obj1, obj2):
		self.debug("distance_beetween_rects_centers")
		x = obj2.center_vector[0] - obj1.center_vector[0]
		y = obj2.center_vector[1] - obj1.center_vector[1]

		if y == 0 or x == 0:
			return x, y, x+y

		return x, y, math.sqrt(((x)**2)+ ((y)**2))

	def get_hipo(self, x, y):
		self.debug("get_hipo")
		return math.sqrt(((x)**2)+ ((y)**2))

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

	def setup_objects(self, objectss, fun=False, fun_info=False):
		self.debug("setup_objects", args=[objectss])
		objects = copy.deepcopy(objectss)
		i = 0
		for o in objects:
			i += 1
			if fun_info:
				fun_info("Adding object n: {}/{}".format(i, len(objects)))

			speed = [0, 0]

			exists = True

			try:
				o["collider"]["movement"]["x"]
			except:
				exists = False

			if exists:
				speed = [o["collider"]["movement"]["x"], o["collider"]["movement"]["y"]]

			o = Object(name="Object", x=o["visual"]["body"]["x"], y=o["visual"]["body"]["y"], static=o["collider"]["static"], speed=speed, width=5, height=5, mass=o["collider"]["mass"], on_collission=False, color=o["visual"]["color"])

			self.objects.append(o)

			if fun:
				fun()

	def __init__(self, debug, get_fps):
		self.debug = debug.get_debug("PHISICS")
		self.debug("__init__")

		self.get_fps = get_fps

		self.fps = 0

		self.distance_scale = 0.5

		self.pause = False

		self.constants = {"G":6.67*10**(-11)}

		self.collider_phisics = True

		self.objects = []
