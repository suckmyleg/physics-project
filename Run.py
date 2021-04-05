import main
import sys

debug_mode = 5

debug_reactive = "Args: %A Id: %I Function_name: %F\n"

log = True

console_log = False

if len(sys.argv) > 1:

	if sys.argv[1].lower() == "true":
		console_log = True

		if len(sys.argv) > 2:
			debug_mode = 2
			debug_reactive = sys.argv[2]

keys_map = [
		["scroll", 4, "zoom_in"],
		["scroll", 5, "zoom_out"],
		["k_down", "k_down", "debug_down"],
		["k_down", "k_up", "debug_up"],
		["k_hold", "k_rshift", "switch_debug"],
		["k_down", "k_escape", "switch_pause"],
		["k_hold", "k_d", "object_move_right"],
		["k_hold", "k_w", "object_move_forward"],
		["k_hold", "k_a", "object_move_left"],
		["k_hold", "k_s", "object_move_back"],
		["k_hold", "k_r", "reload_lvl"]
		]

Simulation = main.Simulation(log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, fps=120, keys_map=keys_map, output_console=console_log)

Simulation.setup()

Simulation.load_lvl(1)

Simulation.start()
