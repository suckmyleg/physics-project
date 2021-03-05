from main.phisics import Phisic
from main.visualizer import Graphic
from time import sleep as sl

class Controller:
	def __init__(self):
		self.graphic = Graphic()
		self.graphic.start_display()
		self.phisics = Phisic(objects=[[[1,3], [2, -5]]])
		for i in range(1):
			o = [self.graphic.make_rect()]
			self.phisics.add_object(o)
			self.graphic.objects.append(o)
		self.graphic.objects = []

	def show_phisics_objects(self):
		self.graphic.show_objects(self.phisics.objects)

	def main(self):
		while True:
			self.show_phisics_objects()
			#print(self.phisics.objects)
			#print("d", d[0][0], d[0][1])
			visuals = []
			for o in self.phisics.objects:
				d = self.phisics.move_object(o, 1, 0)
				visuals.append([[d[0][0], d[0][1]]])

			obj = [[[0,0],self.phisics.get_touch_point(self.phisics.objects[0][0], self.phisics.objects[1][0])]]

			visuals.append(obj)

			print(obj)

			self.graphic.objects = visuals
			#sl(0.1)