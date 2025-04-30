# The MIT License (MIT)
#
# Copyright (c) 2020 ETH Zurich
#
# (License text omitted for brevity...)

import exputil
import time

local_shell = exputil.LocalShell()
max_num_processes = 4

# Check that no screen is running
if local_shell.count_screens() != 0:
    print("There is a screen already running. "
          "Please kill all screens before running this analysis script (killall screen).")
    exit(1)

# Generate the commands

commands_to_run = []

for num_flows in [1, 2, 4, 8]:
    for tcp in ["TcpCubic"]:
        # Starlink
        run_dir = f"runs/starlink_{tcp}_{num_flows}"
        logs_ns3_dir = run_dir + "/logs_ns3"
        local_shell.remove_force_recursive(logs_ns3_dir)
        local_shell.make_full_dir(logs_ns3_dir)
        commands_to_run.append(
            "cd ../../../ns3-sat-sim/simulator; "
            f"./ns3 run \"main_satnet --run_dir=../../paper/ns3_experiments/custom_experiment/{run_dir}\" "
            f"2>&1 | tee '../../paper/ns3_experiments/custom_experiment/{logs_ns3_dir}/console.txt'"
        )

# Run the commands
print("Running commands (at most %d in parallel)..." % max_num_processes)
for i in range(len(commands_to_run)):
    print("Starting command %d out of %d: %s" % (i + 1, len(commands_to_run), commands_to_run[i]))
    local_shell.detached_exec(commands_to_run[i])
    while local_shell.count_screens() >= max_num_processes:
        time.sleep(2)

# Awaiting final completion before exiting
print("Waiting completion of the last %d..." % max_num_processes)
while local_shell.count_screens() > 0:
    time.sleep(2)

print("Finished.")
