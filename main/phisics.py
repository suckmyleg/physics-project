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
		d = self.get_nearest_object_from_object(objectt)

		#print(d[2])

		if d[2] and d[0][2] > 0:
			for l in objectt:
				l = self.move_rect(l, mx, my)



	#MAKE RECTS POINTS 



	def make_point(self, P):
		return np.array([P[0]*self.x, P[1]*self.x])

	def make_rect_from_point_to_angle(self, A, alpha, max=50):
		pass

	def make_rect_from_A_to_B(self, A, B):
		A = self.make_point(A)
		B = self.make_point(B)
		return [A, B, B-A]









	#DISTANCES

	def get_lengths_of_rect(self, rect):
		return abs(rect[0][0]), abs(rect[0][1])


	def get_distance_xy_beetwen_points(self, A, B):
		#print("\nGet_distance")
		#print(A, B)
		r = B - A
		#print(r)
		return abs(r[0]), abs(r[1])

	def get_distance_beetwen_points(self, A, B):
		AB = B-A
		return self.get_hipo(AB[0], AB[1])

	def get_points_from_coord(self, rect, l):
		points = [rect[0], rect[1]]
		for i in range(l):
			points.append(np.array([rect[0][0] + rect[2][0]*i, rect[0][1] + rect[2][1]*i]))
		return points

	def get_points_from_rect(self, rect):
		dx, dy = self.get_distance_xy_beetwen_points(rect[0], rect[1])

		if dx < dy:
			dx = dy

		return self.get_points_from_coord(rect, int(abs(4/2)))


	def get_distance_from_rect_to_rect(self, rect1, rect2):
		points1 = self.get_points_from_rect(rect1)

		points2 = self.get_points_from_rect(rect2)

		#print(points1, points2)

		nearest_points = [False, False, False]

		for p in points1:
			for pp in points2:
				n = self.get_distance_beetwen_points(p, pp)

				#print("aaaaa", n, nearest_points[2])
				if np.array_equal(nearest_points, [False, False, False]):
					nearest_points = [p, pp, n]
				else:
					if n < nearest_points[2]:
						nearest_points = [p, pp, n]

		return nearest_points


	def get_hipo(self, c, a):
		return np.sqrt((c**2)+(a**2))

	def get_nearest_object_from_object(self, objectt):
		nearest = [False, False, False]
		for l in objectt:
			n = self.get_nearest_object_from_rect(l)

			#print("obj", n)

			if np.array_equal(nearest, [False, False, False]):
				nearest = n
			else:
				if not np.array_equal(n, [False, False, False]) and n[0][2] > nearest[0][2]:
					nearest = n

		return nearest

	def get_nearest_object_from_rect(self, rect):
		nearest = [False, False, False]
		for o in self.objects:
			i = 0
			for l in o:
				i += 1
				if not np.array_equal(l, rect):
					P_PP_N = self.get_distance_from_rect_to_rect(rect, l)

					if not nearest[0]:
						nearest = [P_PP_N, l, o]
					else:
						if nearest[0][2] < P_PP_N[2]:
							nearest = [P_PP_N, l, o]
		return nearest


	def __init__(self, objects=[], x=1):
		self.x = x
		self.objects = []
		self.new_objects(objects)
