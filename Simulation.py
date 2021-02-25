from main import Controller

try:
	controller = Controller()
except Exception as e:
	print(e)

try:
	controller.main()
except Exception as e:
	print(e)


input()