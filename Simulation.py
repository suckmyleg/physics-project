from main import Controller

try:
	controller = Controller()
except Exception as e:
	print(e)


controller.main()


input()