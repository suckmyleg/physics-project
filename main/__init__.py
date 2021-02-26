from main.phisics import Phisic
from main.visualizer import Graphic
from time import sleep as sl

class Controller:
	def __init__(self):
		self.graphic = Graphic()
		self.graphic.start_display()
		self.phisics = Phisic([
			[
				[
					[3, 4],
					[5, 6]
				]
			],
			[
				[
					[30,0], 
					[7,200]
				]
			]
			], x=1)

	def show_phisics_objects(self):
		self.graphic.show_objects(self.phisics.objects)

	def main(self):
		while True:
			self.show_phisics_objects()
			d = self.phisics.get_nearest_object_from_rect(self.phisics.objects[0][0])
			self.graphic.print_line(self.phisics.make_rect_from_A_to_B(d[0][0], d[0][1]), color=(100, 250, 0))
			self.phisics.move_object(self.phisics.objects[0], 1, 0)
			sl(0.1)