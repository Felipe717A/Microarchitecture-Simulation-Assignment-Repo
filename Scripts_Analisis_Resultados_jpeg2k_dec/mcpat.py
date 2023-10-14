# mcpat.py
import csv
import os
import subprocess

from config import *

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()
    if process.returncode != 0:
        print(f"Command failed with exit code {process.returncode}")

def main():
    for path_response, path_file in zip(path_response_list, path_file_list):
        try:
            with open(os.path.join(path_file, 'output.csv'), mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row = {k.strip(): v.strip() for k, v in row.items()}
                    uiid = row['unique_id']
                    cmd1 = f"python2 {path_mcpat_build}/gem5toMcPAT_cortexA76.py {path_file}/stats_{uiid}.txt " \
                           f"{path_file}/config_{uiid}.json {path_mcpat_build}/ARM_A76_2.1GHz.xml > {path_response}/config/config_{uiid}.xml"
                    run_command(cmd1)
                    cmd2 = f"{path_mcpat}/mcpat -infile {path_response}/config/config_{uiid}.xml > {path_response}/power/power_data_{uiid}.log"
                    print(cmd2)
                    run_command(cmd2)
        except FileNotFoundError:
            print(f"output.csv not found in {path_file}")


if __name__ == "__main__":
    main()
