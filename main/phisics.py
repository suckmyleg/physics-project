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







	#MOVEMENT FUNCTIONS


	def move_point(self, A, x, y):
		A[0] += x*self.x
		A[1] += y*self.x
		return A

	def move_points(self, points, mx, my):
		for p in points:
			p = self.move_point(p, mx, my)
		return points

	def move_rect(self, rect, mx, my):
		AB = self.move_points([rect[0], rect[1]], mx, my)
		return self.make_rect_from_A_to_B(AB[0], AB[1])

	def move_object(self, objectt, mx, my):
		for l in objectt:
			l = self.move_rect(l, mx, my)



	#MAKE RECTS POINTS 



	def make_point(self, P):
		return np.array([P[0]*self.x, P[1]*self.x, 0])

	def make_rect_from_point_to_angle(self, A, alpha, max=50):
		pass

	def make_rect_from_A_to_B(self, A, B):
		A = self.make_point(A)
		B = self.make_point(B)
		return [A, B, B-A]









	#DISTANCES


	def get_distance_from_rect_to_rect(self, rect1, rect2):

		AB = rect2[0] - rect1[0]

		D1 = rect1[2]

		D2 = rect2[2]

		potencial2 = np.dot(D1, D2)

		#print(potencial2)

		potencial1 = np.linalg.det([AB, D1, D2])

		#print(D1, "\n", D2, "\n")

		return potencial1 / potencial2







	def get_nearest_object_from_rect(self, rect):
		for o in self.objects:
			pass





	def __init__(self, objects=[], x=1):
		self.x = x
		self.objects = []
		self.new_objects(objects)
		