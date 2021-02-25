from main.phisics import Phisic
from main.visualizer import Graphic

class Controller:
	def __init__(self):
		self.graphic = Graphic()
		self.phisics = Phisic([
			[
				[
					[3, 4],
					[5, 6]
				],
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