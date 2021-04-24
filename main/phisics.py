import numpy as np
import math
import copy
from time import sleep

def fix_color(color):
	if color > 260:
		return 260
	else:
		return int(color)

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
	def reload_center(self):
		self.center_vector = [self.x + self.width/2, self.y + self.height/2]

	def setup_vectors(self):
		self.vectors = [
			[self.x, self.y],
			[self.x+self.width, self.y],
			[self.x, self.y+self.height],
			[self.x+self.width, self.y+self.height]
		]


	def __init__(self, phisics, name="Object", id=False, x=0, y=0, speed=[0,0], width=5, height=5, mass=1, static=False, layer=1, color=[255, 0, 0], on_collission=False):
		self.phisics = phisics

		self.name = name

		self.id = id

		self.x = x
		self.y = y

		self.width = width
		self.height = height

		self.mass = mass

		#self.mg = self.mass * self.phisics.constants["G"]

		try:
			self.speed = Force(self, speed[0], speed[1])
		except:
			self.speed = speed

		self.static = static

		self.layer = layer

		self.color = color

		self.setup_vectors()

		self.reload_center()

		self.on_collission = on_collission

	def toList(self):
		return [self.phisics, self.name, self.id, self.x, self.y, self.speed,  self.width, self.height, self.mass, self.static, self.layer, self.color, self.on_collission]

	def interact(self):
		if not self.static:
			for o in self.phisics.objects:
				if not o == self:
					self.interact_with_obj(o)

	def interact_with_obj(self, obj):
		x = (obj.center_vector[0] - self.center_vector[0])*self.phisics.distance_scale
		y = ((obj.center_vector[1] - self.center_vector[1])*self.phisics.distance_scale)

		if y == 0 or x == 0:
			h = x+y
		else:
			h = math.sqrt(((x)**2)+ ((y)**2))

		r = abs(h)

		if r > self.width/2:

			i = 0

			if r > 0:
				i = (obj.mass * self.phisics.constants["G"]/((r*self.phisics.distance_scale)**2))

			angle = self.phisics.get_angle_from_x_y(x, y)

			fx, fy = self.phisics.fx_fy(i, angle)

			self.push([fx, fy])

		else:
			if False and self.speed.total_speed < obj.speed.total_speed:
				self.mass += obj.mass
				self.height += 0.01
				self.width += 0.01
				self.color = [int((self.color[a]+obj.color[a])/2) for a in range(3)]
				#print(self.color)
				self.phisics.remove(obj)

	def stop(self):
		self.speed.stop()

	def move(self, speed):
		self.speed = speed

	def reload(self, fps=1):
		self.interact()
		self.speed.reload(fps=fps)
		self.reload_center()

	def push(self, speed):
		self.speed.push_x_y(speed[0], speed[1])

	def remove(self):
		self.phisics.remove(self)

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
		o.reload(fps=self.fps)

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
		self.debug("real_speed")
		return speed/self.get_fps()

	def push_rect(self, rect, x, y):
		self.debug("push_rect")
		rect["collider"]["movement"]["x"] += self.real_speed(x)
		rect["collider"]["movement"]["y"] += self.real_speed(y)

	def remove(self, o):
		del self.objects[o.id]
		self.reload_objects_ids()

	def fx_fy(self, i, angle):
		self.debug("fx_fy")
		return math.sin(math.radians(angle))*i, math.cos(math.radians(angle))*i

	def get_angle_from_x_y(self, x, y):
		self.debug("get_angle_from_x_y")

		if y == 0:
			if x >= 0:
				return 0
			else:
				return 180

		angle = math.atan(float(x)/float(y))

		angle *= 180/math.pi

		if y < 0:
		   angle += 180

		#print(angle, x, y)

		#print("x:{} y:{} a: {} angle:{}".format(x, y, a, angle))

		return angle

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

	def reload_objects_ids(self):
		for o in self.objects:
			o.id = self.objects.index(o)

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

			o = Object(self, name="Object", x=o["visual"]["body"]["x"], y=o["visual"]["body"]["y"], static=o["collider"]["static"], speed=speed, width=5, height=5, mass=o["collider"]["mass"], on_collission=False, color=o["visual"]["color"])

			self.objects.append(o)

			o.id = self.objects.index(o)

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
