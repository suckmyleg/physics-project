import main

Simulation = main.Simulation(log=True, debug_mode=2, debug_reactive="Args: %A Id: %I Function_name: %F")

Simulation.setup()

Simulation.load(1)

Simulation.start()