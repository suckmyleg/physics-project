import numpy as np

class Phisic:

	def add_object(self, o):
		print("	Adding object:\n 		{}".format(o))
		self.objects.append(o)

	def setup_object(self, o):
		rects = []
		for rect in o:
			rects.append(self.make_rect_from_A_to_B(rect[0], rect[1]))
		return rects

	def new_objects(self, objects):
		print("Adding objects:")
		for o in objects:
			self.add_object(self.setup_object(o))
		print("Done\n")







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
		return np.array([P[0]*self.x, P[1]*self.x, 1])

	def make_rect_from_point_to_angle(self, A, alpha, max=50):
		pass

	def make_rect_from_A_to_B(self, A, B):
		A = self.make_point(A)
		B = self.make_point(B)
		return [A, B, B-A]









	#DISTANCES


	def get_distance_from_rect_to_rect(self, rect1, rect2):

		A = rect1[0]

		B = rect2[0]

		AB = B - A

		AB[2] = 1

		D1 = rect1[2]

		D1[2] = 1

		D2 = rect2[2]

		D2[2] = 1

		potencial2 = np.cross(D1, D2)

		#print(potencial2)

		potencial1 = np.linalg.det([AB, D1, D2])

		#print(D1, "\n", D2, "\n")

		divisor = np.sqrt(potencial2[0]**2+potencial2[1]**2+potencial2[2]**2)

		distance = potencial1/divisor

		#print("Distance: {}".format(distance))

		#print("a: {}\nb: {}\nab: {}\nd1: {}\nd2: {}\npotencial1: {}\npotencial2: {}\ndivisor: {}\n".format(A, B, AB, D1, D2, potencial1, potencial2, divisor))

		return distance







	def get_nearest_object_from_rect(self, rect):
		nearest = [False, False, False]
		for o in self.objects:
			i = 0
			for l in o:
				i += 1
				if not np.array_equal(l, rect):
					n = self.get_distance_from_rect_to_rect(rect, l)

					if not nearest[0]:
						nearest = [n, l, o]
					else:
						if nearest[0] < n:
							nearest = [n, l, o]
		return nearest


	def __init__(self, objects=[], x=1):
		self.x = x
		self.objects = []
		self.new_objects(objects)
		