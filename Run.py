import main
import sys

debug_mode = 3

debug_reactive = "Args: %A Id: %I Function_name: %F\n"

log = False

if len(sys.argv) > 1:

	if sys.argv[1].lower() == "true":
		log = True

		if len(sys.argv) > 2:
			debug_mode = 2
			debug_reactive = sys.argv[2]

keys_map = [
		["scroll", 4, "zoom_in"],
		["scroll", 5, "zoom_out"],
		["k_down", "k_down", "debug_dow"],
		["k_down", "k_up", "debug_up"],
		["k_down", "k_rshift", "switch_debug"],
		["k_down", "k_escape", "switch_pause"],
		["k_hold", "k_d", "player_move_right"],
		["k_hold", "k_w", "player_move_forward"],
		["k_hold", "k_a", "player_move_left"],
		["k_hold", "k_s", "player_move_back"]
		]

Simulation = main.Simulation(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, fps=60, keys_map=keys_map, output_console=True)

Simulation.setup()

Simulation.load(1)

Simulation.start()
