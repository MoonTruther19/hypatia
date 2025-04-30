# The MIT License (MIT)
# (license text omitted for brevity...)

import exputil
import os

local_shell = exputil.LocalShell()

# Prepare directories
local_shell.remove_force_recursive("pdf")
local_shell.make_full_dir("pdf")
local_shell.remove_force_recursive("data")
local_shell.make_full_dir("data")

starlink_cubic = ""
kuiper_cubic = ""

def list_directories(folder_path):
    directories = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories

def process_progress_files(directory):
    global starlink_cubic
    global kuiper_cubic
    file = f"runs/{directory}/logs_ns3/tcp_flows.txt"

    if not os.path.isfile(file):
        print(f"⚠️ Warning: Missing file {file}, skipping.")
        return

    with open(file, 'r') as file:
        lines = file.readlines()
        if lines:
            lines = lines[1:]  # skip header
            count = len(lines)
            for line in lines:
                try:
                    data = f"{int(count)/2},{line.split()[1]},{float(line.split()[9]) / float(line.split()[7]) * 1000}\n"
                    if "starlink" in directory.lower():
                        starlink_cubic += data
                    elif "kuiper" in directory.lower():
                        kuiper_cubic += data
                except (IndexError, ValueError) as e:
                    print(f"⚠️ Skipping malformed line in {file.name}: {line.strip()}")

def plot(folder, id):
    local_shell.perfect_exec(
        "cd ../../../ns3-sat-sim/simulator/contrib/basic-sim/tools/plotting/plot_tcp_flow; "
        "python plot_tcp_flow.py "
        f"../../../../../../../paper/ns3_experiments/custom_experiment/runs/{folder}/logs_ns3 "
        f"../../../../../../../paper/ns3_experiments/custom_experiment/data/{folder} "
        f"../../../../../../../paper/ns3_experiments/custom_experiment/pdf/{folder} "
        f"{id} " + str(1 * 1000 * 1000 * 1000),  # 1s interval
        output_redirect=exputil.OutputRedirect.CONSOLE
    )

# Main
directories = list_directories("runs")

for directory in directories:
    process_progress_files(directory)

# Plot first 2 flows for Starlink and Kuiper Cubic
for prefix in ["kuiper"]:
    plot(f"{prefix}_TcpCubic_1", 0)
    plot(f"{prefix}_TcpCubic_1", 1)

# Write aggregated CSVs
# with open("data/starlink_cubic.csv", 'w') as f:
#     f.write(starlink_cubic)

with open("data/kuiper_cubic.csv", 'w') as f:
    f.write(kuiper_cubic)
