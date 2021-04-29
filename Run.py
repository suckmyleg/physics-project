import main
import sys

debug_mode = 5

debug_reactive = "Args: %A Id: %I Function_name: %F\n"

log = False

console_log = False

if len(sys.argv) > 1:

	if sys.argv[1].lower() == "true":
		log = True

	if len(sys.argv) > 2:
		debug_mode = 2
		debug_reactive = sys.argv[2]

keys_map = [
		["scroll", 4, "debug_zoom_in"],
		["scroll", 5, "debug_zoom_out"],
		["k_down", "k_down", "debug_down"],
		["k_down", "k_up", "debug_up"],
		["k_hold", "k_rshift", "switch_debug"],
		["k_hold", "k_escape", "switch_pause"],
		["k_hold", "k_d", "object_move_right"],
		["k_hold", "k_w", "object_move_forward"],
		["k_hold", "k_a", "object_move_left"],
		["k_hold", "k_s", "object_move_back"],
		["k_hold", "k_r", "reload_lvl"],
		["click", 1, "spawn_new_rect"],
		["k_hold", "k_l", "less_distance"],
		["k_hold", "k_k", "more_distance"],
		["k_hold", "k_f", "change_lvl"],
		["k_hold", "k_c", "input_console"],
		["k_hold", "k_i", "switch_objects_speeds"],
		["k_hold", "k_b", "spawn_new_black_hole"],
		["k_hold", "k_n", "spawn_new_rect"],
		["k_hold", "k_t", "main.start"]
		

		]

Simulation = main.Simulation(log, log=log, debug_mode=debug_mode, debug_reactive=debug_reactive, fps=6000, keys_map=keys_map, output_console=console_log, output_file=True, debug_interval_time=10)

Simulation.setup()

Simulation.load_lvl(5)

Simulation.start()
