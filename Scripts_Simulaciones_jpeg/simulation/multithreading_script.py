import concurrent.futures
import shutil
import subprocess
import time
import csv
from config import *
import uuid


# You need to run simulate.sh first
with open(OUTPUT_FILE, 'w') as f:
    f.write("l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries, cpi, ipc, unique_id\n")

def is_blacklisted(l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries):
    try:
        with open(BLACKLIST_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == [l1i_size, str(l1i_assoc), l2_size, str(l2_assoc), l3_size, str(l3_assoc), str(fetch_width), str(decode_width), str(rob_entries)]:
                    return True
        return False
    except FileNotFoundError:
        return False

def blacklist_combination(l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries):
    with open(BLACKLIST_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries])

def get_existing_combinations():
    existing_combinations = set()
    try:
        with open(OUTPUT_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                combination = tuple(row[:6])
                existing_combinations.add(combination)
        return existing_combinations
    except FileNotFoundError:
        return set()

def run_simulation(l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries):
    try:
        MOREOPTIONS = f"--l1i_size={l1i_size} --l1i_assoc={l1i_assoc} --l2_size={l2_size} --l2_assoc={l2_assoc} --l3_size={l3_size} --l3_assoc={l3_assoc} --fetch_width={fetch_width} --decode_width={decode_width} --rob_entries={rob_entries}"

        command = f"{GEM5PATH}/gem5.fast {SCRIPTPATH}/CortexA76.py --cmd={CMD} --options={OPTIONS} {MOREOPTIONS}"

        print(f"Executing: {command}")
        process = subprocess.Popen(command, shell=True)
        process.wait()
        if process.returncode != 0:
            print(f"Command failed with exit code {process.returncode}")

        while not os.path.exists(f"{OUTPUT_DIR}/stats.txt"):
            time.sleep(1)

        with open(f"{OUTPUT_DIR}/stats.txt") as stats_file:
            cpi = None
            ipc = None
            for line in stats_file:
                if "system.cpu.cpi" in line:
                    cpi = line.split()[1]
                elif "system.cpu.ipc" in line:
                    ipc = line.split()[1]

        if cpi is None or ipc is None or cpi == 'inf':
            print(
                f"Warning: CPI or IPC values not found for parameters {l1i_size}, {l1i_assoc}, {l2_size}, {l2_assoc}, {l3_size}, {l3_assoc},{fetch_width}, {decode_width}, {rob_entries}")
            blacklist_combination(l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries)
            return
        unique_id = str(uuid.uuid4())
        new_file_stats = f"{OUTPUT_DIR}/stats_{unique_id}.txt"
        new_file_config = f"{OUTPUT_DIR}/config_{unique_id}.json"
        shutil.copy(f"{OUTPUT_DIR}/stats.txt", new_file_stats)
        shutil.copy(f"{OUTPUT_DIR}/config.json", new_file_config)
        os.remove(f"{OUTPUT_DIR}/stats.txt")
        os.remove(f"{OUTPUT_DIR}/config.json")

        with open(OUTPUT_FILE, 'a') as f:
            f.write(
                f"{l1i_size}, {l1i_assoc}, {l2_size}, {l2_assoc}, {l3_size}, {l3_assoc}, {fetch_width}, {decode_width}, {rob_entries}, {cpi}, {ipc}, {unique_id}\n")


    except Exception as e:
        print(f"Error occurred in simulation with parameters {l1i_size}, {l1i_assoc}, {l2_size}, {l2_assoc}, {l3_size}, {l3_assoc}, {fetch_width}, {decode_width}, {rob_entries}: {e}")

if __name__ == "__main__":
    iteration_counter = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        futures = []

        existing_combinations = get_existing_combinations()
        l3_assoc = 32
        for l1i_size in cache_sizes_L1:
            for l1i_assoc in assocs_L1:
                for l2_size in cache_sizes_L2:
                    for l2_assoc in assocs_L2:
                        for l3_size in cache_sizes_L3:
                            for fetch_width in fetch_width_values:
                                for decode_width in decode_width_values:
                                    for rob_entries in rob_entries_values:
                                        combination = (l1i_size, str(l1i_assoc), l2_size, str(l2_assoc), l3_size, str(l3_assoc), str(fetch_width), str(decode_width), str(rob_entries))
                                        if not is_blacklisted(*combination) and combination not in existing_combinations:
                                            futures.append(
                                                executor.submit(run_simulation, l1i_size, l1i_assoc, l2_size, l2_assoc, l3_size, l3_assoc, fetch_width, decode_width, rob_entries))

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                iteration_counter += 1
            except Exception as exc:
                print(f'Generated an exception: {exc}')