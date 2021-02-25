import numpy as np

class Phisic:

	def add_object(self, o):
		print("Adding object:\n{}".format(o))
		self.objects.append(o)

	def setup_object(self, o):
		rects = []
		for rect in o:
			rects.append(self.make_rect_from_A_to_B(rect[0], rect[1]))
		return rects

	def new_objects(self, objects):
		for o in objects:
			self.add_object(self.setup_object(o))










	def move_point(self, A, x, y):
		A[0] += x
		A[1] += y
		return A

	def move_points(self, points, mx, my):
		for p in points:
			p = self.move_point(p, mx, my)
		return points



	def make_point(self, P):
		return np.array([P[0]*self.x, P[1]*self.x])


	def move_rect(self, rect):
		AB = self.move_point([rect[0], rect[1]])
		rect[0] = AB[0]
		rect[1] = AB[1]
		return rect

	def make_rect_from_point_to_angle(self, A, alpha, max=50):
		pass

	def make_rect_from_A_to_B(self, A, B):
		A = self.make_point(A)
		B = self.make_point(B)
		return [A, B, B-A]




	def get_nearest_rect_from_object(self):



	def get_nearest_object_from_rect(self, rect):
		for o in self.objects:






	def __init__(self, objects=[], x=1):
		self.x = x
		self.objects = []
		self.new_objects(objects)
		