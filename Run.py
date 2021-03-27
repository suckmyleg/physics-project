import main
import sys

debug_mode = 0

debug_reactive = "Args: %A Id: %I Function_name: %F\n"

if len(sys.argv) > 1:
	debug_mode = 2
	debug_reactive = sys.argv[1]

Simulation = main.Simulation(log=True, debug_mode=debug_mode, debug_reactive=debug_reactive)

while True:

	Simulation.setup()

	Simulation.load(1)

	Simulation.start()

	Simulation.visuals.main()
