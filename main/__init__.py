from main.phisics import Phisic
from main.visualizer import Graphic
from time import sleep as sl

class Controller:
	def __init__(self):
		self.graphic = Graphic()
		self.phisics = Phisic([
			[
				[
					[3, 4],
					[5, 6]
				]
			],
			[
				[
					[4,3], 
					[7,8]
				]
			]
			], x=100)

	def show_phisics_objects(self):
		self.graphic.show_objects(self.phisics.objects)

	def main(self):
		while True:
			self.show_phisics_objects()
			print(self.phisics.get_distance_from_rect_to_rect(self.phisics.objects[0][0], self.phisics.objects[1][0]))
			self.phisics.move_object(self.phisics.objects[0], 0.01, 0)
			sl(0.1)